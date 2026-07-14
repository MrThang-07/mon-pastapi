from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base # Giả định Base đã được khai báo từ hệ thống

# 1. Bảng trung gian cho quan hệ Nhiều - Nhiều (Student - Course)
student_course = Table(
    "student_course", 
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

# 2. Khai báo các Model
class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    # =========================================================================
    # [LỖI 1: Quan hệ 1-N] - Lỗi tham chiếu đồng bộ ngược (back_populates)
    # - Nguyên nhân: back_populates phải trỏ đến TÊN BIẾN relationship ở class 
    #   đối diện (Student), không phải tên cột khóa ngoại (department_id).
    # - Cách khắc phục: Đổi "department_id" thành "department".
    # =========================================================================
    students = relationship("Student", back_populates="department")


class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    
    # Thiết lập khóa ngoại trỏ về Department
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="students")
    
    # =========================================================================
    # [LỖI 2: Quan hệ 1-1] - Thiếu giới hạn object ở tầng ORM
    # - Nguyên nhân: Mặc định relationship trả về 1 list (1-N). Để thành 1-1, 
    #   ORM cần biết chỉ trả về 1 object duy nhất.
    # - Cách khắc phục: Thêm tham số uselist=False.
    # =========================================================================
    profile = relationship("Profile", back_populates="student", uselist=False)
    
    # =========================================================================
    # [LỖI 3: Quan hệ N-N] - Thiếu cấu hình bảng trung gian
    # - Nguyên nhân: Quan hệ N-N không thể tự nối trực tiếp mà phải thông qua 
    #   bảng phụ (student_course), nhưng code cũ chưa khai báo nó vào relationship.
    # - Cách khắc phục: Thêm tham số secondary=student_course.
    # =========================================================================
    courses = relationship("Course", secondary=student_course, back_populates="students")

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String(255))
    
    # =========================================================================
    # [LỖI 2: Quan hệ 1-1] - Thiếu ràng buộc duy nhất ở tầng Database
    # - Nguyên nhân: Nếu không có unique=True, 1 student_id có thể xuất hiện 
    #   nhiều lần trong bảng profiles, phá vỡ quy tắc 1-1.
    # - Cách khắc phục: Thêm unique=True vào khai báo ForeignKey.
    # =========================================================================
    student_id = Column(Integer, ForeignKey("students.id"), unique=True)
    student = relationship("Student", back_populates="profile")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    
    # =========================================================================
    # [LỖI 3: Quan hệ N-N] - Thiếu cấu hình bảng trung gian (chiều ngược lại)
    # - Cách khắc phục: Tương tự class Student, thêm secondary=student_course 
    #   vào chiều này để đồng bộ.
    # =========================================================================
    students = relationship("Student", secondary=student_course, back_populates="courses")