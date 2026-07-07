from database import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

# Khai bao model anh xa du lieu voi CSDL
class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)


# Khai bao model de nhan du lieu tu nguoi dung
class StudentRequetsDTO(BaseModel):
    id: int
    full_name: str
    email: str