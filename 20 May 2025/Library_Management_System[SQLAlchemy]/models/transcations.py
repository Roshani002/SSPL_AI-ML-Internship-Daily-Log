from sqlalchemy import Column, Integer, Date, DECIMAL, ForeignKey, func
from models.base import Base

class Transcation(Base):
    __tablename__ = 'transcations'
    transcation_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    issue_date = Column(Date)
    due_date = Column(Date)
    return_date = Column(Date, server_default=func.current_date())
    # fineamount = Column(DECIMAL(10,2))


