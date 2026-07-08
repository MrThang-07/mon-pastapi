from database import *
from sqlalchemy import Column, Integer , Boolean,String
class UsersModel(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False,unique=True)
    