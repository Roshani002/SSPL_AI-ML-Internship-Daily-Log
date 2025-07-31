from fetch_transform_data import fetch_data_api, transform_data
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from news_table import Base, News
from typing import List

class DatabaseConnect:
    def __init__(self, db_url='sqlite:///database/news.db'):
        self.db_url = db_url
        self.engine = create_engine(self.db_url)
        self.session_factory = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
    
    def load_data(self, loaded_data: List[News]):
        session = self.session_factory()
        try:
            session.begin()
            session.add_all(loaded_data)
            session.commit()
        except Exception as e:
            print(f"Error: {e}")
            session.rollback()
        finally:
            session.close()