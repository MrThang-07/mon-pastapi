from pydantic import BaseModel, Field ,EmailStr
from typing import Literal

class StudentBase(BaseModel):
    student_code: str = Field(..., min_length=3, max_length=20)
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    # cài pydantic[email]
    age: int = Field(..., ge=16, le=60)
    gender: Literal["male", "female", "other"]
    class_id: int = Field(..., ge=1)

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

# Nested Schema (Lồng thông tin lớp học)
class ClassroomResponse(BaseModel):
    id: int
    class_code: str
    class_name: str

    class Config:
        from_attributes = True  # Thay thế cho orm_mode=True ở Pydantic v2

class StudentResponse(StudentBase):
    id: int
    classroom: ClassroomResponse

    class Config:
        from_attributes = True