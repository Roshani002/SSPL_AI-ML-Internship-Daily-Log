# import asyncio
# import logging
# import sys
# from mcp.server.fastmcp import FastMCP
# from database import init_db, close_db
# from tools.users import create_user, transfer_user_to_department
# from resources.users import fetch_recent_users, fetch_users_by_criteria

# # configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("mcp_server")

# # Create MCP Server
# server = FastMCP("DatabaseMCP")

# # Register the resources
# @server.resource("http://127.0.0.1:8000/recent_users", name="recent_users", description="Fetch recent users")
# async def recent_users_resource():
#     return await fetch_recent_users(limit=10)

# @server.resource(
#     "http://127.0.0.1:8000/users_by_criteria",
#     name="users_by_criteria", 
#     description="Fetch users matching specific criteria like department or role."
# )
# async def users_by_criteria_resource():
#     return await fetch_users_by_criteria(
#         department=None,
#         role=None,
#         active=True,
#         limit=10
#     )



# async def create_user_handler(username: str, email: str, department: str = "General", role: str = "User"):
#     """Create a new user in the database."""
#     data = {
#         "username": username,
#         "email": email,
#         "department": department,
#         "role": role
#     }
#     return await create_user(data)

# async def transfer_user_handler(user_id: int, new_department: str):
#     """Transfer a user to a new department."""
#     if not user_id or not new_department:
#         return {"error": "Missing user_id or new_department"}
    
#     return await transfer_user_to_department(user_id, new_department)

# # Register tools with proper handlers
# server.tool("create_user", "Create a new user in the database.")(create_user_handler)
# server.tool("transfer_user", "Transfer a user to a new department.")(transfer_user_handler)


# async def main():
#     try:
#         await init_db()
#         logger.info("Database initialized successfully")
#         logger.info("Starting MCP Server with SQLite DB")
#         await server.run()
#     except Exception as e:
#         logger.error(f"Server error: {e}")
#     finally:
#         logger.info("Shutting down server...")
#         await close_db()

# if __name__ == "__main__":
#     asyncio.run(main())

#!/usr/bin/env python3
"""Standard MCP Server implementation"""

import asyncio
import logging
import json
import sys
from typing import Any, Sequence
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from pydantic import AnyUrl

# Import your database functions
from database import init_db, close_db
from tools.users import create_user, transfer_user_to_department
from resources.users import fetch_recent_users, fetch_users_by_criteria

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp_server")

# Create server instance
server = Server("DatabaseMCP")

@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri=AnyUrl("db://recent_users"),
            name="Recent Users",
            description="Get the most recent users from the database",
            mimeType="application/json",
        ),
        Resource(
            uri=AnyUrl("db://users_by_criteria"),
            name="Users by Criteria",
            description="Get users matching specific criteria (department, role, active status)",
            mimeType="application/json",
        ),
    ]

@server.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """Read a specific resource."""
    try:
        if str(uri) == "db://recent_users":
            logger.info("Reading recent users resource")
            users = await fetch_recent_users(limit=10)
            return json.dumps(users, indent=2, default=str)
        
        elif str(uri) == "db://users_by_criteria":
            logger.info("Reading users by criteria resource")
            users = await fetch_users_by_criteria()
            return json.dumps(users, indent=2, default=str)
        
        else:
            raise ValueError(f"Unknown resource: {uri}")
            
    except Exception as e:
        logger.error(f"Error reading resource {uri}: {e}")
        return json.dumps({"error": str(e)}, indent=2)

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_recent_users",
            description="Get the most recent users from the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer", 
                        "description": "Maximum number of users to return (default: 10)", 
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="get_users_by_criteria",
            description="Get users matching specific criteria (department, role, active status)",
            inputSchema={
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string", 
                        "description": "Filter by department (e.g., Engineering, Marketing, Sales, HR, Support)"
                    },
                    "role": {
                        "type": "string", 
                        "description": "Filter by role (e.g., Developer, Manager, Representative, Recruiter)"
                    },
                    "active": {
                        "type": "boolean", 
                        "description": "Filter by active status (true for active users, false for inactive)", 
                        "default": True
                    },
                    "limit": {
                        "type": "integer", 
                        "description": "Maximum number of users to return (default: 10)", 
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="create_user",
            description="Create a new user in the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string", 
                        "description": "Unique username for the new user (3-50 chars, alphanumeric + underscore)"
                    },
                    "email": {
                        "type": "string", 
                        "description": "Valid email address for the user"
                    },
                    "department": {
                        "type": "string", 
                        "description": "Department name (e.g., Engineering, Marketing, Sales)", 
                        "default": "General"
                    },
                    "role": {
                        "type": "string", 
                        "description": "User role (e.g., Developer, Manager, Representative)", 
                        "default": "User"
                    },
                },
                "required": ["username", "email"],
            },
        ),
        Tool(
            name="transfer_user",
            description="Transfer a user to a new department and log the change",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer", 
                        "description": "ID of the user to transfer"
                    },
                    "new_department": {
                        "type": "string", 
                        "description": "Name of the new department"
                    },
                },
                "required": ["user_id", "new_department"],
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls."""
    try:
        logger.info(f"Tool called: {name} with args: {arguments}")
        
        if name == "get_recent_users":
            limit = arguments.get("limit", 10)
            result = await fetch_recent_users(limit=limit)
            logger.info(f"get_recent_users result: {len(result) if isinstance(result, list) else 'error'}")
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
        elif name == "get_users_by_criteria":
            department = arguments.get("department")
            role = arguments.get("role")
            active = arguments.get("active", True)
            limit = arguments.get("limit", 10)
            
            result = await fetch_users_by_criteria(
                department=department,
                role=role,
                active=active,
                limit=limit
            )
            logger.info(f"get_users_by_criteria result: {len(result) if isinstance(result, list) else 'error'}")
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
        elif name == "create_user":
            result = await create_user(arguments)
            logger.info(f"create_user result: {result}")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "transfer_user":
            user_id = arguments.get("user_id")
            new_department = arguments.get("new_department")
            
            if not user_id or not new_department:
                result = {"status": "error", "message": "Missing user_id or new_department"}
            else:
                result = await transfer_user_to_department(user_id, new_department)
            
            logger.info(f"transfer_user result: {result}")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Tool {name} error: {e}")
        error_result = {"status": "error", "message": str(e)}
        return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

async def main():
    """Main server function."""
    try:
        logger.info("Starting MCP Server initialization...")
        
        # Initialize database first
        await init_db()
        logger.info("Database initialized successfully")
        
        # Test database connection
        from database import get_db_connection
        db = await get_db_connection()
        if db:
            logger.info("Database connection verified")
            # Test a simple query
            async with db.execute("SELECT COUNT(*) as count FROM users") as cursor:
                row = await cursor.fetchone()
                user_count = row["count"] if row else 0
                logger.info(f"Database contains {user_count} users")
        else:
            raise Exception("Database connection failed")
        
        logger.info("Starting MCP Server on stdio...")
        logger.info("Server is ready to accept connections")
        
        # Start the stdio server
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, 
                write_stream, 
                server.create_initialization_options()
            )
    
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        try:
            logger.info("Shutting down server...")
            await close_db()
            logger.info("Database closed successfully")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Fatal server error: {e}")
        sys.exit(1)