from fastapi import APIRouter , Depends 
from sqlalchemy.orm import Session 
from database import get_db
import app.services.student_service as student_service
from app.schemas.student_schema import StudentResponse
student_router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

# API de lay sinh vien
@student_router.get("/", response_model= StudentResponse)
def get_all_student(offset:int = 0 , limit:int = 3 ,db : Session = Depends(get_db)):
    return {
        "message": "lAY DU LIEU THANH CONG",
        "data": student_service.get_all_student(db , offset , limit)
    }

@student_router.get("/{student_id}", response_model=StudentResponse)
def get_student(student:int ,db : Session = Depends(get_db) ):
    return student_service.get_student(db ,student)

