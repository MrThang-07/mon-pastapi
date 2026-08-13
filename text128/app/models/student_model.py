from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from database import Base

# ==========================================
# 1. QUAN HỆ 1-1: Người dùng (User) - Hồ sơ (UserProfile)
# Ý nghĩa: 1 User chỉ có 1 Profile, và 1 Profile chỉ thuộc về 1 User.
# ==========================================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    
    # [QUAN HỆ 1-1 CẤP CODE]
    # - uselist=False là TỪ KHÓA BẮT BUỘC để tạo quan hệ 1-1. 
    # - Nó báo cho SQLAlchemy biết: "Khi gọi user.profile, chỉ trả về 1 object duy nhất, đừng trả về một mảng (list)".
    # - back_populates="user" để móc nối 2 chiều với biến 'user' ở class UserProfile bên dưới.
    profile = relationship("UserProfile", back_populates="user", uselist=False)

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    
    # [KHÓA NGOẠI 1-1 CẤP DATABASE]
    # - ForeignKey("users.id"): Khóa ngoại nối vào cột id của bảng users.
    # - unique=True: Đây là điểm mấu chốt! Đảm bảo không có 2 dòng profile nào được phép trỏ chung về 1 user_id.
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    address = Column(String(200))
    
    # [QUAN HỆ 1-1 CẤP CODE] (Từ phía Profile ngược lại)
    user = relationship("User", back_populates="profile")


# ==========================================
# 2. QUAN HỆ 1-N: Lớp học (Classroom) - Sinh viên (Student)
# Ý nghĩa: 1 Lớp có NHIỀU Sinh viên, nhưng 1 Sinh viên chỉ thuộc 1 Lớp.
# ==========================================
class Classroom(Base):
    __tablename__ = "classrooms"
    id = Column(Integer, primary_key=True, index=True)
    class_code = Column(String(50), unique=True, index=True, nullable=False)
    class_name = Column(String(100), nullable=False)
    max_students = Column(Integer, nullable=False)
    status = Column(String(20), default="active")

    # [QUAN HỆ 1-N CẤP CODE] (Phía 1)
    # - Không có uselist=False, nên mặc định khi gọi classroom.students, SQLAlchemy sẽ trả về 1 LIST chứa nhiều sinh viên.
    students = relationship("Student", back_populates="classroom")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    student_code = Column(String(20), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum("male", "female", "other", name="gender_enum"), nullable=False)
    
    # [KHÓA NGOẠI 1-N CẤP DATABASE] (Phía N)
    # - Khóa ngoại LUÔN LUÔN nằm ở bảng "Nhiều". 
    # - Cột class_id nối với bảng classrooms để biết sinh viên này thuộc lớp nào.
    class_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)

    # [QUAN HỆ 1-N CẤP CODE] (Từ phía N nhìn về phía 1)
    # - Biến 'classroom' (số ít) sẽ trả về 1 object Classroom tương ứng với class_id ở trên.
    classroom = relationship("Classroom", back_populates="students")
    
    # Chuẩn bị móc nối cho quan hệ N-N ở bên dưới
    enrollments = relationship("Enrollment", back_populates="student")


# ==========================================
# 3. QUAN HỆ N-N: Sinh viên (Student) - Môn học (Course) 
# Ý nghĩa: 1 SV đăng ký NHIỀU Môn học, và 1 Môn học có NHIỀU SV.
# Bắt buộc phải có BẢNG TRUNG GIAN (Enrollment) đứng giữa.
# ==========================================
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(50), unique=True, nullable=False)
    course_name = Column(String(100), nullable=False)

    # Móc nối sang bảng trung gian
    enrollments = relationship("Enrollment", back_populates="course")


# [BẢNG TRUNG GIAN]
# Bản chất của quan hệ N-N trong CSDL là hai mối quan hệ 1-N chụm lại vào 1 bảng giữa.
class Enrollment(Base):
    __tablename__ = "enrollments"
    
    # [KHÓA CHÍNH KÉP & KHÓA NGOẠI]
    # - Bảng trung gian kéo 'id' của sinh viên và 'id' của môn học về làm 2 khóa ngoại (ForeignKey).
    # - Đồng thời, dùng cả 2 cột này làm khóa chính (primary_key=True) nhằm mục đích: 
    #   1 Sinh viên không thể đăng ký 1 môn học tới 2 lần (Chống trùng lặp tuyệt đối).
    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    
    enroll_date = Column(Date, nullable=False)

    # [QUAN HỆ 1-N CẤP CODE TỪ BẢNG TRUNG GIAN]
    # Trỏ ngược về bảng Student và Course để SQLAlchemy biết đường nối bảng (JOIN) khi lấy dữ liệu.
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")