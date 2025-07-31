import logging
from database import get_db_connection
from typing import List, Optional, Dict, Any

logger = logging.getLogger("mcp_database.resources.users")

async def fetch_recent_users(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch the most recent users from the database

    Args:
        limit: Maximum number of users to return (default: 10)

    Returns: 
        List of user objects or an error dict.
    """

    try:
        db_connection = await get_db_connection()
        if not db_connection:
            logger.error("Database not initialized")
            return {"error": "Database connection not available"}

    
        query = """
        SELECT id, username, email, department, role, created_at
        FROM users
        ORDER BY datetime(created_at) DESC
        LIMIT ?
        """
        async with db_connection.execute(query, (limit,)) as cursor:
            rows = await cursor.fetchall()
        users = [dict(row) for row in rows]
        logger.info(f"Fetched {len(users)} recent users (limit={limit})")
        return users
    except Exception as e:
        logger.error(f"Error fetching recent users: {e}")
        return {"error": f"Database error: {e}"}

async def fetch_users_by_criteria(
    department: Optional[str] = None,
    role: Optional[str] = None,
    active: Optional[bool] = True,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Fetch users matching specific criteria (SQLite version).
    
    Args:
        department: Filter by department (optional)
        role: Filter by role (optional)
        active: Filter by active status (default: True)
        limit: Maximum results to return (default: 10)
        
    Returns:
        List of matching user objects
    """
    try:
        db_connection = await get_db_connection()
        if not db_connection:
            logger.error("Database connection not available")
            return {"error": "Database connection not available"}

        # Build dynamic query
        conditions = ["active = ?"]
        params: list[Any] = [1 if active else 0]  # SQLite stores booleans as integers

        if department:
            conditions.append("department = ?")
            params.append(department)

        if role:
            conditions.append("role = ?")
            params.append(role)
        params.append(limit)
        query = f"""
            SELECT id, username, email, department, role, created_at 
            FROM users 
            WHERE {' AND '.join(conditions)}
            ORDER BY created_at DESC 
            LIMIT ?;
        """
        
        async with db_connection.execute(query, params) as cursor:
            rows = await cursor.fetchall()

        # Convert sqlite Row objects to dicts
        users = [dict(r) for r in rows] 
        logger.info(f"Fetched {len(users)} users matching criteria")
        return users

    except Exception as e:
        logger.error(f"Error fetching users by criteria: {e}")
        return {"error": f"Database error: {str(e)}"}
    
