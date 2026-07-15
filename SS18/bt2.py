# ==============================================================================
# BÀI TẬP: QUẢN LÝ LỚP HỌC VÀ SINH VIÊN
# Tóm tắt phân tích lỗi cũ:
# 1. API GET /classrooms/{id}: Thiếu .filter() lấy sinh viên, dẫn đến lấy ALL sinh viên.
# 2. API PUT /students/{id}/transfer: Thiếu validate (student null, classroom null,
#    classroom CLOSED) và sai logic check sức chứa (dùng > thay vì >=).
# ==============================================================================

from typing import List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship,
    Session
)

# --- CẤU HÌNH DATABASE ---
DATABASE_URL = "sqlite:///./classroom.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()

# --- MODEL DATABASE (SQLALCHEMY) ---
class Classroom(Base):
    __tablename__ = "classrooms"
    
    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)
    capacity = Column(Integer, nullable=False)
    
    students = relationship(
        "Student",
        back_populates="classroom"
    )

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_code = Column(String(20), nullable=False)
    full_name = Column(String(100), nullable=False)
    classroom_id = Column(
        Integer,
        ForeignKey("classrooms.id"),
        nullable=False
    )
    
    classroom = relationship(
        "Classroom",
        back_populates="students"
    )

Base.metadata.create_all(bind=engine)

# --- SCHEMAS (PYDANTIC) ---
class ClassroomCreate(BaseModel):
    class_name: str
    status: str
    capacity: int

class StudentCreate(BaseModel):
    student_code: str
    full_name: str
    classroom_id: int

class TransferClassRequest(BaseModel):
    new_classroom_id: int

class StudentResponse(BaseModel):
    id: int
    student_code: str
    full_name: str
    classroom_id: int
    model_config = ConfigDict(from_attributes=True)

class ClassroomDetailResponse(BaseModel):
    id: int
    class_name: str
    status: str
    capacity: int
    students: List[StudentResponse] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)

# --- KHỞI TẠO FASTAPI ---
app = FastAPI(title="Classroom Student API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API ENDPOINTS ---

@app.post("/classrooms")
def create_classroom(data: ClassroomCreate, db: Session = Depends(get_db)):
    classroom = Classroom(
        class_name=data.class_name,
        status=data.status,
        capacity=data.capacity
    )
    db.add(classroom)
    db.commit()
    db.refresh(classroom)
    return classroom

@app.post("/students", response_model=StudentResponse)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    classroom = db.query(Classroom).filter(Classroom.id == data.classroom_id).first()
    if classroom is None:
        raise HTTPException(status_code=404, detail="Lớp học không tồn tại")
    
    if classroom.status != "OPEN":
        raise HTTPException(status_code=400, detail="Lớp học đã đóng")
    
    current_count = db.query(Student).filter(Student.classroom_id == data.classroom_id).count()
    if current_count >= classroom.capacity:
        raise HTTPException(status_code=400, detail="Lớp học đã đủ sinh viên")
    
    student = Student(
        student_code=data.student_code,
        full_name=data.full_name,
        classroom_id=data.classroom_id
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

# ---------------------------------------------------------
# API ĐÃ SỬA: Lấy chi tiết lớp học
# ---------------------------------------------------------
@app.get("/classrooms/{classroom_id}", response_model=ClassroomDetailResponse)
def get_classroom_detail(classroom_id: int, db: Session = Depends(get_db)):
    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    
    if classroom is None:
        raise HTTPException(status_code=404, detail="Lớp học không tồn tại")
    
    # [FIX] Đã thêm .filter() để chỉ lấy đúng sinh viên của lớp học này
    # Mã cũ gọi .all() không có điều kiện sẽ lấy toàn bộ sinh viên trong CSDL
    students = (
        db.query(Student)
        .filter(Student.classroom_id == classroom_id) 
        .order_by(Student.id)
        .all()
    )
    
    return {
        "id": classroom.id,
        "class_name": classroom.class_name,
        "status": classroom.status,
        "capacity": classroom.capacity,
        "students": students
    }

# ---------------------------------------------------------
# API ĐÃ SỬA: Chuyển lớp học
# ---------------------------------------------------------
@app.put("/students/{student_id}/transfer", response_model=StudentResponse)
def transfer_student(student_id: int, data: TransferClassRequest, db: Session = Depends(get_db)):
    # 1. Tìm sinh viên (Tránh lỗi 500 nếu sinh viên không tồn tại)
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")

    # 2. Tìm lớp học đích (Tránh lỗi 500 khi check status/capacity ở bước sau)
    target_classroom = db.query(Classroom).filter(Classroom.id == data.new_classroom_id).first()
    if target_classroom is None:
        raise HTTPException(status_code=404, detail="Lớp học đích không tồn tại")

    # 3. [FIX] Kiểm tra trạng thái lớp đích (Chặn chuyển vào lớp CLOSED)
    if target_classroom.status == "CLOSED":
        raise HTTPException(status_code=400, detail="Lớp học đã đóng")

    # 4. Đếm số sinh viên hiện tại của lớp đích
    current_count = db.query(Student).filter(Student.classroom_id == data.new_classroom_id).count()
    
    # 5. [FIX] Kiểm tra sức chứa (Phải dùng >=, mã cũ dùng > khiến lớp đủ người vẫn lọt)
    if current_count >= target_classroom.capacity:
        raise HTTPException(status_code=400, detail="Lớp học đã đủ sinh viên")

    # 6. Cập nhật ID lớp học mới cho sinh viên và lưu lại
    student.classroom_id = data.new_classroom_id
    db.commit()
    db.refresh(student)
    
    return student