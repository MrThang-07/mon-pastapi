from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# 1. Khuôn mẫu gốc chứa các trường chung
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

# 2. Schema dùng khi đăng ký 
class UserCreate(UserBase):
    password: str

# 3. Schema dùng khi trả dữ liệu về (UserResponse)
class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    # Bật tính năng tự động map dữ liệu từ Database Model sang Pydantic
    class Config:
        from_attributes = True