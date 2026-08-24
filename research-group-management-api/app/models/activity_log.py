from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.db.database import Base 

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)        # "CREATE_PROJECT", "UPDATE_PROJECT"
    description = Column(String(255), nullable=False)  
    created_at = Column(DateTime, default=datetime.utcnow)