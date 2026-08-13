from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, Any
from datetime import datetime, timezone

from database import get_db
from app.schemas import student_schema
from app.services import student_service

router = APIRouter(prefix="/students", tags=["Sinh Viên"])

def format_response(request: Request, status_code: int, message: str, data: Any = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "message": message,
            "data": data if data is not None else {},
            "error": None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": request.url.path
        }
    )

@router.get("")
def get_list_students(request: Request, search: Optional[str] = None, class_id: Optional[int] = None, db: Session = Depends(get_db)):
    students = student_service.get_students(db, search, class_id)
    # Nếu không có dữ liệu, trả về danh sách rỗng []
    data = [student_schema.StudentResponse.model_validate(s).model_dump() for s in students]
    return format_response(request, 200, "Lấy danh sách thành công", data=data)

@router.get("/{student_id}")
def get_student_detail(request: Request, student_id: int, db: Session = Depends(get_db)):
    student = student_service.get_student_by_id(db, student_id)
    data = student_schema.StudentResponse.model_validate(student).model_dump()
    return format_response(request, 200, "Lấy chi tiết thành công", data=data)

@router.post("", status_code=201)
def create_new_student(request: Request, student_in: student_schema.StudentCreate, db: Session = Depends(get_db)):
    student = student_service.create_student(db, student_in)
    data = student_schema.StudentResponse.model_validate(student).model_dump()
    return format_response(request, 201, "Thêm mới thành công", data=data)

@router.put("/{student_id}")
def update_existing_student(request: Request, student_id: int, student_in: student_schema.StudentUpdate, db: Session = Depends(get_db)):
    student = student_service.update_student(db, student_id, student_in)
    data = student_schema.StudentResponse.model_validate(student).model_dump()
    return format_response(request, 200, "Cập nhật thành công", data=data)