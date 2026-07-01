
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


students_db = [
    {"id": 1, "name": "Nguyen Van A", "age": 20},
    {"id": 2, "name": "Tran Thi B", "age": 21}
]
class StudentUpdate(BaseModel):
    name: str
    age: int

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students_db:
        if student.get("id") == student_id:
            students_db.remove(student)
            return {"status": "Xoa thanh cong"}
            
    return {"status": "Khong tim thay sinh vien"}



@app.put("/students/{student_id}")
def update_student(student_id: int, updated_data: StudentUpdate):
    for student in students_db:
        if student["id"] == student_id:
            student["name"] = updated_data.name
            student["age"] = updated_data.age
            return {"status": "Cap nhat thanh cong", "data": student}
            
    return {"status": "Khong tim thay sinh vien"}