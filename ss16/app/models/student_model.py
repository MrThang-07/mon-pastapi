from database import Base
# Import thêm Table để tạo bảng trung gian
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

# =====================================================================
# BẢNG TRUNG GIAN CHO MỐI QUAN HỆ NHIỀU - NHIỀU (Sinh viên - Môn học)
# =====================================================================
student_course_table = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("tables.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

# =====================================================================
# BẢNG DEPARTMENT (MỐI QUAN HỆ 1 - NHIỀU với Sinh viên)
# =====================================================================
class DepartmentModel(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    # 1 Khoa có nhiều Sinh viên
    students = relationship("table_database", back_populates="department")

# =====================================================================
# BẢNG COURSE (MỐI QUAN HỆ NHIỀU - NHIỀU với Sinh viên)
# =====================================================================
class CourseModel(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    # 1 Môn học có nhiều Sinh viên (dùng bảng trung gian student_course_table)
    students = relationship("table_database", secondary=student_course_table, back_populates="courses")

# =====================================================================
# BẢNG SINH VIÊN (Chứa tất cả các mối quan hệ)
# =====================================================================
class table_database(Base):
    __tablename__ = "tables"
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)

    # 1. Liên kết 1 - 1 (Code cũ của bạn)
    profile = relationship("ProfileModel", back_populates="student", uselist=False)

    # 2. Liên kết 1 - Nhiều (Sinh viên thuộc về 1 Khoa)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("DepartmentModel", back_populates="students")

    # 3. Liên kết Nhiều - Nhiều (Sinh viên học nhiều Môn)
    courses = relationship("CourseModel", secondary=student_course_table, back_populates="students")

# =====================================================================
# BẢNG PROFILE (MỐI QUAN HỆ 1 - 1 với Sinh viên)
# =====================================================================
class ProfileModel(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    bio = Column(String(100))
    
    # Tạo khóa ngoại (Code cũ của bạn)
    student_id = Column(Integer, ForeignKey("tables.id"), unique=True)
    student = relationship("table_database", back_populates="profile")