# class User:
#     def __init__(self, id, name, email, phonenumber, address, membership_date):
#         self.id = id
#         self.name = name
#         self.email = email
#         self.phonenumber = phonenumber
#         self.address= address
#         self.membership_date = membership_date

from sqlalchemy import Column, Integer, String, Date
from models.base import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phonenumber = Column(Integer)
    address = Column(String)
    membership_date = Column(Date)



