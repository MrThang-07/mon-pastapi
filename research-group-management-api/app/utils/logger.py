from sqlalchemy.orm import Session
from app.models.activity_log import ActivityLog

def log_activity(db: Session, user_id: int, action: str, description: str):
    new_log = ActivityLog(
        user_id=user_id,
        action=action,
        description=description
    )
    db.add(new_log)
    db.commit()