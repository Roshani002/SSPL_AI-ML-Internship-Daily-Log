from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from models.books import Book
from models.users import User
from models.transcations import Transcation
from models.base import Base

class DatabaseManager:
    def __init__(self, db_url='sqlite:///database/library.db'):
        self.db_url = db_url
        self.engine = None
        self.session_factory = None

    def setup_database(self):
        """Initializes engine, creates all tables, and sets up sessionmaker."""
        self.engine = create_engine(self.db_url)
        Base.metadata.create_all(bind=self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        print("Database setup complete and tables created.")

    def get_session(self):
        """Returns a new session."""
        if not self.session_factory:
            raise Exception("Database not set up. Call setup_database() first.")
        return self.session_factory()

