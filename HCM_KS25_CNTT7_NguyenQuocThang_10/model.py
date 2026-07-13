from database import Base
from sqlalchemy import Column , String , Integer,Float
class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True,autoincrement=True, index=True)
    full_name = Column(String(255),nullable=False)
    department = Column(String(255),nullable=False)
    position = Column(String(255),nullable=False)
    salary = Column(Float, nullable=False)