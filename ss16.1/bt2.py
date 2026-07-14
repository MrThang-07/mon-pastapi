"""
===================================================================================
PHẦN 1: BÁO CÁO LỖI CẤU HÌNH (TÓM TẮT)
===================================================================================

1. Lỗi tham chiếu đồng bộ ngược / Quan hệ 1-N (Phòng ban <-> Nhân viên)
   - Vị trí gây lỗi: Dòng `employees = relationship("Employee", back_populates="department_id")` trong class Department.
   - Nguyên nhân: Thuộc tính `back_populates` phải trỏ đến TÊN BIẾN relationship ở class đối diện (tức là biến `department` trong class Employee), không được trỏ vào tên cột khóa ngoại.
   - Cách khắc phục: Sửa `back_populates="department_id"` thành `back_populates="department"`.

2. Lỗi thiếu ràng buộc tính duy nhất / Quan hệ 1-1 (Nhân viên <-> Thiết bị)
   - Vị trí gây lỗi: Khai báo biến `device` (class Employee) và khóa ngoại `employee_id` (class Device).
   - Nguyên nhân: Mặc định ForeignKey tạo quan hệ 1-N. Để giới hạn thành 1-1 thực sự, phải khóa ở 2 đầu: tầng DB không cho trùng lặp, tầng ORM chỉ cho phép trả về 1 object.
   - Cách khắc phục: 
     + Class Employee: Thêm `uselist=False` vào `relationship()`.
     + Class Device: Thêm `unique=True` vào `Column(..., ForeignKey(...))`.

3. Lỗi thiếu cấu hình bảng trung gian / Quan hệ N-N (Nhân viên <-> Dự án)
   - Vị trí gây lỗi: Khai báo biến `projects` (class Employee) và `employees` (class Project).
   - Nguyên nhân: Quan hệ Nhiều - Nhiều không thể liên kết trực tiếp hai bảng. Khai báo thiếu tham số trỏ tới bảng trung gian khiến SQLAlchemy không biết cách nối dữ liệu.
   - Cách khắc phục: Thêm tham số `secondary=employee_project` vào khai báo `relationship` ở cả hai class.

===================================================================================
PHẦN 2: SOURCE CODE ĐÃ SỬA HOÀN CHỈNH
===================================================================================
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base # Giả định Base đã được khai báo từ hệ thống

# 1. Bảng trung gian cho quan hệ Nhiều - Nhiều (Employee - Project)
employee_project = Table(
    "employee_project", 
    Base.metadata,
    Column("employee_id", Integer, ForeignKey("employees.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True)
)

# 2. Khai báo các Model
class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    # [ĐÃ SỬA LỖI 1]: Đổi "department_id" thành "department"
    employees = relationship("Employee", back_populates="department")

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    # Thiết lập khóa ngoại trỏ về Department
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="employees")
    
    # [ĐÃ SỬA LỖI 2]: Thêm uselist=False để thiết lập quan hệ 1-1 ở tầng ORM
    device = relationship("Device", back_populates="employee", uselist=False)
    
    # [ĐĐ SỬA LỖI 3]: Thêm tham số secondary để trỏ tới bảng trung gian
    projects = relationship("Project", secondary=employee_project, back_populates="employees")

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(50), unique=True, nullable=False)
    
    # [ĐÃ SỬA LỖI 2]: Thêm unique=True để ép tính duy nhất ở tầng Database
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True)
    employee = relationship("Employee", back_populates="device")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    
    # [ĐÃ SỬA LỖI 3]: Thêm tham số secondary vào chiều ngược lại của quan hệ N-N
    employees = relationship("Employee", secondary=employee_project, back_populates="projects")