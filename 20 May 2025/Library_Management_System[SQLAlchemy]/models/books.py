# class Book:
#     def __init__(self, name, author, published_year, genre, available):
#         self.name = name
#         self.author = author
#         self.published_year = published_year
#         self.genre = genre
#         self.available = available

from sqlalchemy import Column, Integer, String
from models.base import Base

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    book_name = Column(String)
    author = Column(String)
    published_year = Column(Integer)
    genre = Column(String)
    available = Column(Integer)

