import os
import aiosqlite
import logging
from dotenv import load_dotenv

load_dotenv()

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp_database")


DB_PATH = os.getenv("DB_PATH", "company.db")
db_connection: aiosqlite.Connection = None

# create tables
CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL DEFAULT 'General',
    role TEXT NOT NULL DEFAULT 'User',
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS user_audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    field_changed TEXT NOT NULL,
    old_value TEXT NOT NULL,
    new_value TEXT NOT NULL,
    changed_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

# Insert data
INSERT_DATA_SQL = """
-- Insert 10 sample users
INSERT OR IGNORE INTO users (username, email, department, role, active)
VALUES 
  ('alice','alice@example.com','Engineering','Developer', 1),
  ('bob','bob@example.com','Marketing','Manager', 0),
  ('carol','carol@example.com','Sales','Representative', 1),
  ('dave','dave@example.com','HR','Recruiter', 1),
  ('eve','eve@example.com','Engineering','Tester', 1),
  ('frank','frank@example.com','Support','Agent', 0),
  ('grace','grace@example.com','Engineering','DevOps', 1),
  ('heidi','heidi@example.com','Product','Designer', 1),
  ('ivan','ivan@example.com','Legal','Lawyer', 0),
  ('judy','judy@example.com','Finance','Accountant', 1);

-- Insert corresponding audit logs (assuming the order of IDs is from 1 to 10)
INSERT OR IGNORE INTO user_audit_log (user_id, field_changed, old_value, new_value)
VALUES
  (1, 'role', 'Intern', 'Developer'),
  (2, 'department', 'Sales', 'Marketing'),
  (3, 'role', 'Intern', 'Representative'),
  (4, 'role', 'Intern', 'Recruiter'),
  (5, 'department', 'QA', 'Engineering'),
  (6, 'role', 'Intern', 'Agent'),
  (7, 'department', 'Ops', 'Engineering'),
  (8, 'role', 'Intern', 'Designer'),
  (9, 'role', 'Intern', 'Lawyer'),
  (10, 'department', 'Accounts', 'Finance');
"""

async def get_db_connection():
    """Get the database connection, ensuring it's initialized."""
    global db_connection
    if db_connection is None:
        await init_db()
    return db_connection

async def init_db():
    """Initialize the database connection."""
    global db_connection
    try:
        if db_connection is not None:
            logger.info("Database already initialized")
            return
            
        db_connection = await aiosqlite.connect(DB_PATH)
        db_connection.row_factory = aiosqlite.Row
        logger.info(f"Connected to SQLite at {DB_PATH}")
    
        # create tables if they don't exist
        await db_connection.executescript(CREATE_TABLES_SQL)
        logger.info("Ensured users & user_audit_log tables exist")

        # Insert data
        await db_connection.executescript(INSERT_DATA_SQL)
        await db_connection.commit()
        logger.info("Inserted data into both tables")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def close_db():
    """Close the database connection"""
    global db_connection
    if db_connection:
        await db_connection.close()
        db_connection = None
        logger.info("Closed SQLite connection")