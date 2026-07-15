# pyrefly: ignore [missing-import]
from sqlalchemy import Column, String, Integer, ForeignKey, Table
# pyrefly: ignore [missing-import]
from database import Base
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship

# Middle table
student_course = Table(
    "student_courses",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))

    # Link by 1-1 relationship
    # Link the relationship by the trick
    profile = relationship("ProfileModel", back_populates="student", uselist=False)
    department = relationship("DepartmentModel", back_populates="students")
    courses = relationship("CourseModel", secondary=student_course, back_populates="students")


class ProfileModel(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bio = Column(String(100))
    # Create foreign key
    student_id = Column(Integer, ForeignKey("students.id"), unique=True)
    # Links in the reverse direction
    student = relationship("StudentModel", back_populates="profile")


# Create a Department table associated with a student table with a 1 multiple relationship
class DepartmentModel(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    students = relationship("StudentModel", back_populates="department")

# Create a course table associated with a student table with multiple relationships
class CourseModel(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    students = relationship("StudentModel", secondary=student_course, back_populates="courses")