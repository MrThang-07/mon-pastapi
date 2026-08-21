from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    """
    Dữ liệu đầu vào khi Đăng ký tài khoản.
    Bao gồm email, họ tên và mật khẩu thô.
    """
    password: str

class UserLogin(BaseModel):
    """
    Dữ liệu đầu vào khi Đăng nhập.
    Chỉ cần email và mật khẩu.
    """
    email: EmailStr
    password: str

class UserResponse(UserBase):
    """
    Dữ liệu trả về cho client. 
    TUYỆT ĐỐI KHÔNG trả về mật khẩu, chỉ trả về các thông tin an toàn.
    """
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        # Giúp Pydantic có thể đọc dữ liệu trực tiếp từ SQLAlchemy Model object
        from_attributes = True