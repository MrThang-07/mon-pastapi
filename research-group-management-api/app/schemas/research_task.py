from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ResearchTaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.TODO
    priority: Optional[TaskPriority] = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

# Schema dùng khi TẠO task
class ResearchTaskCreate(ResearchTaskBase):
    pass

# Schema dùng khi CẬP NHẬT task 
class ResearchTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None

# Schema dùng khi TRẢ VỀ dữ liệu cho Frontend 
class ResearchTaskResponse(ResearchTaskBase):
    id: int
    project_id: int
    assignee_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True