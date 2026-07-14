from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from database import get_db
import app.services.student_service as student_service
student_router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

# API de lay sinh vien
@student_router.get("/")
def get_all_student(db : Session = Depends(get_db)):
    return {
        "message": "lAY DU LIEU THANH CONG",
        "data": student_service.get_all_student(db)
    }
