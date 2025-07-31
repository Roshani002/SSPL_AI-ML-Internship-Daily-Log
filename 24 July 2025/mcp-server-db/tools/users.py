import logging
import re
import aiosqlite
from typing import Dict, Any, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from database import get_db_connection

logger = logging.getLogger("mcp_database.tools.users")

class CreateUserRequest(BaseModel):
    """Validation model for user creation."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    department: Optional[str] = "General"
    role: Optional[str] = "User"

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must be alphanumeric or underscore')
        return v

async def create_user(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Insert a new user securely into the database.

    Args:
        data: Dict containing username, email, department, role.

    Returns:
        Dict with status, message, and optional user_id or error.
    """
    # Validate input
    try:
        user = CreateUserRequest(**data)
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return {"status": "error", "message": f"Validation failed: {e}"}

    try:
        db_connection = await get_db_connection()
        if not db_connection:
            logger.error("Database connection not available")
            return {"status": "error", "message": "Database not available"}

    
        # Check for existing user
        query = """
        SELECT id FROM users
        WHERE username = ? OR email = ?
        """
        async with db_connection.execute(query, (user.username, user.email)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {"status": "error", "message": "User with this username or email already exists"}

        # Insert new user - 
        insert_sql = """
        INSERT INTO users (username, email, department, role, active)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor = await db_connection.execute(insert_sql,
            (user.username, user.email, user.department, user.role, 1))
        await db_connection.commit()
        user_id = cursor.lastrowid

        logger.info(f"Created new user: {user.username} (ID: {user_id})")
        return {"status": "success", "message": f"User {user.username} created", "user_id": user_id}

    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return {"status": "error", "message": f"Database insertion failed: {e}"}
    

logger = logging.getLogger(__name__)

async def transfer_user_to_department(
    user_id: int,
    new_department: str
) -> Dict[str, Any]:
    """
    Transfer a user to a new department, recording the change in the audit log.
    
    Args:
        user_id: ID of the user to transfer
        new_department: Name of the target department
        
    Returns:
        Status of the operation
    """
    try:
        db_connection = await get_db_connection()
        if not db_connection:
            return {"status": "error", "message": "DB connection not available"}
        
        # fetch current
        sql_get = "SELECT department FROM users WHERE id=?;"
        async with db_connection.execute(sql_get, (user_id,)) as cur:
            row = await cur.fetchone()
        if not row:
            return {"status": "error", "message": "User not found"}
        current = row["department"]
        
        # transaction
        await db_connection.execute("BEGIN;")
        await db_connection.execute("UPDATE users SET department=? WHERE id=?;", (new_department, user_id))
        await db_connection.execute(
            "INSERT INTO user_audit_log (user_id,field_changed,old_value,new_value) VALUES (?,?,?,?);",
            (user_id, "department", current, new_department)
        )
        await db_connection.commit()
        return {"status": "success", "message": f"Moved from {current} to {new_department}"}

    except Exception as e:
        logger.error(f"Error transferring user: {e}")
        return {"status": "error", "message": f"Database error: {e}"}