from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title = "Manager Student"
)
student_dtb = [
    {"id": 1, "username": "Việt Thành" , "password" :"123"},
    {"id": 2, "username": "giahung" , "password" :"456"}
]
# định hình dữ liệu nhập vào
class StudentSchema(BaseModel):
    id : int
    username : str
    password : str

# lấy ds sinh viên
# @app.get("/students", tags=["Students"], summary="Lấy danh sách sinh viên")
# def get_all_students():
#     return {
#         "status_code": 200,
#         "message": "Lấy danh sách sinh viên thành công",
#         "data": student_dtb
#     }
# thêm sinh viên
@app.post("/students", tags=["Students"], summary="thêm danh sách sinh viên")
def create_students(student: StudentSchema):
    student_id = len(student_dtb) + 1
    news_student = {
        "id": student_id,
        "username": student.username,
        "password": student.password
    }
    student_dtb.append(news_student)
    return{
        "status_code": 201,
        "massage": "Thêm thành công",
        "data": news_student
    }
#  lấy 1 sinh viên 
@app.get("/students/{student_id}", tags=["Students"], summary="xóa sinh viên")
def get_student_by_id(student_id: int):
    for stu in student_dtb:
        if stu.get("id") == student_id:
            return {
                "message": "Lấy thành công",
                "data": stu
            }
        return {
            "message": "không tìm thấy"
        }

    
