from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# CƠ SỞ DỮ LIỆU GIẢ LẬP
students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]

courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2}
]

registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1}
]

class RegistrationCreate(BaseModel):
    student_id: int
    course_id: int


# ==============================================================================
# PHẦN 1: PHÂN TÍCH VÀ THIẾT KẾ GIẢI PHÁP
#
# 1. Phân tích bài toán:
#    - Input: JSON body gồm 2 trường: student_id (int) và course_id (int).
#    - Output thành công: Trả về HTTP Status 201 Created kèm dữ liệu phiếu đăng ký mới.
#    - Output thất bại: Trả về lỗi HTTPException (400 hoặc 404) kèm lý do chi tiết.
#
# 2. Đề xuất giải pháp (Luồng xử lý):
#    - B1: Kiểm tra student_id xem học viên có tồn tại trong hệ thống không.
#    - B2: Kiểm tra course_id xem khóa học có tồn tại và lấy ra sức chứa (capacity).
#    - B3 (Bẫy 1): Quét danh sách registrations xem học viên đã đăng ký khóa này chưa.
#    - B4 (Bẫy 2): Đếm số học viên hiện tại của khóa học, nếu >= capacity thì báo đầy lớp.
#    - B5: Nếu vượt qua hết các bước trên, tiến hành tạo mới bản ghi dữ liệu.
# ==============================================================================


# ==============================================================================
# PHẦN 2: TRIỂN KHAI CODE API
# ==============================================================================
@app.post("/registrations", status_code=status.HTTP_201_CREATED)
def create_registration(reg: RegistrationCreate):
    
    # Bước 1: Kiểm tra học viên tồn tại
    student_exists = False
    for s in students:
        if s.get("id") == reg.student_id:
            student_exists = True
            break
    if not student_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    # Bước 2: Kiểm tra khóa học tồn tại & Lấy thông tin khóa học
    target_course = None
    for c in courses:
        if c.get("id") == reg.course_id:
            target_course = c
            break
    if not target_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    # Bước 3 (Bẫy 1): Kiểm tra học viên bị đăng ký trùng khóa học
    for r in registrations:
        if r.get("student_id") == reg.student_id and r.get("course_id") == reg.course_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Student already registered this course"
            )

    # Bước 4 (Bẫy 2): Kiểm tra sĩ số khóa học (Capacity)
    current_slots = 0
    for r in registrations:
        if r.get("course_id") == reg.course_id:
            current_slots += 1
            
    if current_slots >= target_course.get("capacity"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Course is full"
        )

    # Bước 5: Tạo mới dữ liệu khi hoàn toàn hợp lệ
    new_reg = {
        "id": len(registrations) + 1,
        "student_id": reg.student_id,
        "course_id": reg.course_id
    }
    
    registrations.append(new_reg)
    return {
        "message": "Registration created successfully",
        "data": new_reg
    }