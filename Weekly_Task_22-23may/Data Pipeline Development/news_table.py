from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Date, TIMESTAMP

class Base(DeclarativeBase):
    pass

class News(Base):
    __tablename__ = "news"
    news_id = Column(Integer, primary_key=True)
    source = Column(String, default= "BBC News")
    title = Column(String)
    description = Column(String)
    url = Column(String)
    published_at = Column(TIMESTAMP)
    content = Column(String)