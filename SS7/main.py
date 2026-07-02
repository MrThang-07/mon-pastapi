from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title = "Manager Students",
)
# Định nghĩa dữ liệu client gửi lên.
class StudentRequestDTO(BaseModel):
    username: str
    email: str
    password: str

# Định nghĩa dữ liệu trả về cho client.
class StudentResponseDTO(BaseModel):
    username: str
    email: str


students_dtb = [
    {"id": 1, "username": "GiaHung", "email": "giahung@gmail.com", "password": "123"},
    {"id": 2, "username": "GiaKhanh", "email": "giakhanh@gmail.com", "password": "456"},
    {"id": 3, "username": "MinhDuc", "email": "minhduc@gmail.com", "password": "789"},
]

# Thêm sinh viên
@app.post("/students", tags=["Students"], status_code=status.HTTP_201_CREATED)
def create_students(student: StudentRequestDTO):
    student_id = len(students_dtb) + 1
    new_student = {
        "id": student_id,
        "username": student.username, 
        "email": student.email, 
        "password": student.password
    }

    students_dtb.append(new_student)
    return {
        "status_code": status.HTTP_201_CREATED,
        "message": "Thêm thành công",
        "data": new_student
    }

# API Lấy sinh viên theo ID
@app.get("/students/{student_id}", tags=["Students"], status_code=status.HTTP_200_OK, response_model=StudentResponseDTO)
def get_student(student_id: int):
    student_find = next((s for s in students_dtb if s.get("id") == student_id), None)
    if student_find is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy"
        )
    # return {
    #     "status_code": status.HTTP_200_OK,
    #     "message": "Lấy thành công",
    #     "data": student_find
    # }
    return student_find