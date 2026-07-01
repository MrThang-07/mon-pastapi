from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="API Quản Lý Học Viên Cơ Bản")

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]

class Student(BaseModel):
    id: int
    code: str
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    age: int = Field(..., gt=0)

@app.get("/students")
def get_students(keyword: str = None, min_age: int = None, max_age: int = None):
    if keyword == None and min_age == None and max_age == None:
        return students
    
    ket_qua = []
    
    for s in students:
        giu_lai = True
        
        if keyword != None:
            kw = keyword.lower()
            if (kw not in s["name"].lower()) and (kw not in s["code"].lower()) and (kw not in s["email"].lower()):
                giu_lai = False
                
        if min_age != None:
            if s["age"] < min_age:
                giu_lai = False
                
        if max_age != None:
            if s["age"] > max_age:
                giu_lai = False
                
        if giu_lai == True:
            ket_qua.append(s)
            
    return ket_qua

@app.get("/students/{student_id}")
def get_student_detail(student_id: int):
    for s in students:
        if s["id"] == student_id:
            return s
            
    raise HTTPException(status_code=404, detail="Student not found")

@app.post("/students")
def create_student(student: Student):
    for s in students:
        if s["code"] == student.code:
            raise HTTPException(status_code=400, detail="Mã học viên (code) đã bị trùng")
        if s["id"] == student.id:
            raise HTTPException(status_code=400, detail="ID đã bị trùng")
            
    students.append(student.dict())
    return {"message": "Thêm học viên thành công", "data": student.dict()}

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    for s in students:
        if s["code"] == student.code and s["id"] != student_id:
            raise HTTPException(status_code=400, detail="Mã học viên (code) bị trùng với người khác")

    for i in range(len(students)):
        if students[i]["id"] == student_id:
            students[i]["code"] = student.code
            students[i]["name"] = student.name
            students[i]["email"] = student.email
            students[i]["age"] = student.age
            return {"message": "Cập nhật thành công", "data": students[i]}
            
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for i in range(len(students)):
        if students[i]["id"] == student_id:
            deleted_student = students.pop(i)
            return {"message": "Xóa thành công", "data": deleted_student}
            
    raise HTTPException(status_code=404, detail="Student not found")