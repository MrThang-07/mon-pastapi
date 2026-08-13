from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.models import Student, Classroom
from app.schemas.student_schema import StudentCreate, StudentUpdate

def get_students(db: Session, search: str = None, class_id: int = None):
    query = db.query(Student)
    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            (Student.full_name.ilike(search_fmt)) |
            (Student.student_code.ilike(search_fmt)) |
            (Student.email.ilike(search_fmt))
        )
    if class_id:
        query = query.filter(Student.class_id == class_id)
    return query.all()

def get_student_by_id(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")
    return student

def create_student(db: Session, student_in: StudentCreate):
    # Kiểm tra lớp học
    classroom = db.query(Classroom).filter(Classroom.id == student_in.class_id).first()
    if not classroom:
        raise HTTPException(status_code=400, detail="Lớp học không tồn tại")
    if classroom.status != "active":
        raise HTTPException(status_code=400, detail="Lớp học không hoạt động")
    if len(classroom.students) >= classroom.max_students:
        raise HTTPException(status_code=400, detail="Lớp học đã đủ số lượng sinh viên")

    # Kiểm tra trùng lặp
    if db.query(Student).filter(Student.student_code == student_in.student_code).first():
        raise HTTPException(status_code=400, detail="Mã sinh viên đã tồn tại")
    if db.query(Student).filter(Student.email == student_in.email).first():
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    new_student = Student(**student_in.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

def update_student(db: Session, student_id: int, student_in: StudentUpdate):
    student = get_student_by_id(db, student_id)

    # Kiểm tra trùng lặp với người khác
    if db.query(Student).filter(Student.student_code == student_in.student_code, Student.id != student_id).first():
        raise HTTPException(status_code=400, detail="Mã sinh viên trùng với sinh viên khác")
    if db.query(Student).filter(Student.email == student_in.email, Student.id != student_id).first():
        raise HTTPException(status_code=400, detail="Email trùng với sinh viên khác")

    # Kiểm tra chuyển lớp
    if student.class_id != student_in.class_id:
        new_classroom = db.query(Classroom).filter(Classroom.id == student_in.class_id).first()
        if not new_classroom:
            raise HTTPException(status_code=400, detail="Lớp học mới không tồn tại")
        if new_classroom.status != "active":
            raise HTTPException(status_code=400, detail="Lớp học mới không hoạt động")
        if len(new_classroom.students) >= new_classroom.max_students:
            raise HTTPException(status_code=400, detail="Lớp học mới đã đầy")

    for key, value in student_in.model_dump().items():
        setattr(student, key, value)
    
    db.commit()
    db.refresh(student)
    return student