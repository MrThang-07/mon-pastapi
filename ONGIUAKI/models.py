from database import Base
from sqlalchemy import Integer,String,Column
class Team(Base):
    __tablename__ = "__teams__"
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    country_name = Column(String(100),nullable=False)
    coach_name = Column(String(100),nullable=False)
    group_name = Column(String(100),nullable=False)