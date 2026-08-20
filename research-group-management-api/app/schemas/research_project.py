from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ==========================
# SCHEMA CHO ĐỀ TÀI (PROJECT)
# ==========================
class ResearchProjectBase(BaseModel):
    name: str
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
class ResearchMemberResponse(BaseModel):
    project_id: int
    user_id: int
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True