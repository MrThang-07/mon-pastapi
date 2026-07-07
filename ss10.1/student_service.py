from sqlalchemy.orm import Session
from model import *

def create_students(db: Session, student: StudentRequetsDTO):
    try:
        new_student = StudentModel(
            id = student.id,
            full_name = student.full_name,
            email = student.email
        )
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        return {
            "status_code": 201,
            "message": "Tao sinh vien thanh cong"
        }
    except Exception as e:
        db.rollback()
        raise ValueError(f"Loi khi tao sinh vien: {str(e)}")
    
def get_all_students(db: Session):
    try:
        # Khởi tạo truy vấn trên StudentModel và lấy tất cả kết quả
        students = db.query(StudentModel).all()
        return students
    except Exception as e:
        # Bắt lỗi nếu có sự cố truy vấn
        raise ValueError(f"Lỗi khi lấy danh sách sinh viên: {str(e)}")