from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# 1. DỮ LIỆU GIẢ LẬP BAN ĐẦU
enrollments = [
    {
        "id": 1,
        "student_id": "SV001",
        "course_id": 1
    },
    {
        "id": 2,
        "student_id": "SV002",
        "course_id": 1
    }
]

# 2. MODEL PYDANTIC HỨNG DỮ LIỆU
class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: int


# ==============================================================================
# PHÂN TÍCH LỖI LOGIC CỦA CODE CŨ:
# 1. Thiếu vòng lặp để đối chiếu đồng thời cả 'student_id' và 'course_id' với dữ liệu cũ,
#    dẫn đến việc một học viên có thể đăng ký lặp đi lặp lại cùng một khóa học nhiều lần.
# 2. Phản hồi sai chuẩn HTTP Status Code (Trả về mã 200 OK mặc định thay vì 201 Created).
# ==============================================================================

# 3. CODE SAU KHI SỬA LỖI
@app.post("/enrollments", status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment: EnrollmentCreate):
    
    for e in enrollments:
        if e.get("student_id") == enrollment.student_id and e.get("course_id") == enrollment.course_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Hoc vien '{enrollment.student_id}' da dang ky khoa hoc code {enrollment.course_id} nay roi!"
            )
            
    new_enrollment = {
        "id": len(enrollments) + 1,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    }
    
    enrollments.append(new_enrollment)
    return {
        "message": "Enroll successfully",
        "data": new_enrollment
    }