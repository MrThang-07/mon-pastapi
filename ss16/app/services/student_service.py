from sqlalchemy.orm import Session
from app.models.student_model import table_database
def get_all_student(db: Session):
    return db.query(table_database).all()