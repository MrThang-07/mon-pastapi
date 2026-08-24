from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# ==========================
# ĐỊNH NGHĨA ENUM CHUẨN DB
# ==========================
class MemberRole(str, Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"

# ==========================
# SCHEMA CHO ĐỀ TÀI (PROJECT)
# ==========================
class ResearchProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class ResearchProjectCreate(ResearchProjectBase):
    pass  # Dùng luôn các trường của Base để tạo

class ResearchProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ResearchProjectResponse(ResearchProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ==========================
# SCHEMA CHO THÀNH VIÊN (MEMBER)
# ==========================
# Khuôn hứng ID khi Owner muốn thêm thành viên mới
class ResearchMemberAdd(BaseModel):
    user_id: int

# Khuôn trả về thông tin thành viên
class ResearchMemberResponse(BaseModel):
    project_id: int
    user_id: int
    role: MemberRole # Đã áp dụng Enum thay cho chuỗi str thường
    joined_at: datetime

    class Config:
        from_attributes = True