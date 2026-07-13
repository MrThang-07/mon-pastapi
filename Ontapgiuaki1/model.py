from database import Base
from sqlalchemy import String , Column , Integer
class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer , primary_key=True , autoincrement=True,index=True)
    country_name = Column(String(255),nullable=False)
    coach_name = Column(String(255),nullable=False)
    group_name = Column(String(255),nullable=False)