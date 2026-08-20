from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResearchTaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "TODO"
    priority: Optional[str] = "MEDIUM"
    due_date: Optional[datetime] = None

class ResearchTaskCreate(ResearchTaskBase):
    pass

class ResearchTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None

class ResearchTaskResponse(ResearchTaskBase):
    id: int
    project_id: int
    assignee_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True