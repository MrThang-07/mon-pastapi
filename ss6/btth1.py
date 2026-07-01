from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="API Quản Lý Khóa Học Cơ Bản")

# Đây là một List (Danh sách). Nó chứa 3 khóa học ban đầu.
courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

# Kiểm tra điều kiện đầu vào
class Course(BaseModel):
    id: int
    code: str
    name: str = Field(..., min_length=1)  # Không được rỗng
    duration: int = Field(..., gt=0)      # Lớn hơn 0
    fee: int = Field(..., ge=0)           # Lớn hơn hoặc bằng 0


# --- TÌM KIẾM VÀ LỌC ---
@app.get("/courses")
def get_courses(keyword: str = None, min_fee: int = None, max_fee: int = None):
    # 1. Nếu không tìm kiếm gì cả -> Trả về toàn bộ danh sách
    if keyword == None and min_fee == None and max_fee == None:
        return courses
    
    # 2. Tạo một cái hộp rỗng để chứa những khóa học đúng yêu cầu
    ket_qua = []
    
    # Dùng vòng lặp lấy từng khóa học (c) ra để xét
    for c in courses:
        giu_lai = True  # Ban đầu mặc định là cho phép khóa học này qua ải
        
        # Ải 1: Xét keyword
        if keyword != None:
            # Nếu keyword không nằm trong tên VÀ không nằm trong code -> Loại
            if (keyword.lower() not in c["name"].lower()) and (keyword.lower() not in c["code"].lower()):
                giu_lai = False
                
        # Ải 2: Xét tiền tối thiểu
        if min_fee != None:
            if c["fee"] < min_fee:  # Tiền khóa học nhỏ hơn mức tối thiểu -> Loại
                giu_lai = False
                
        # Ải 3: Xét tiền tối đa
        if max_fee != None:
            if c["fee"] > max_fee:  # Tiền khóa học lớn hơn mức tối đa -> Loại
                giu_lai = False
                
        # Nếu qua hết các ải mà vẫn là True -> Bỏ vào hộp kết quả
        if giu_lai == True:
            ket_qua.append(c)
            
    return ket_qua


# --- XEM CHI TIẾT 1 KHÓA HỌC ---
@app.get("/courses/{course_id}")
def get_course_detail(course_id: int):
    # Tìm xem có khóa học nào có id trùng với course_id không
    for c in courses:
        if c["id"] == course_id:
            return c
            
    # Nếu chạy hết vòng lặp mà không thấy thì báo lỗi
    raise HTTPException(status_code=404, detail="Course not found")


# --- THÊM KHÓA HỌC ---
@app.post("/courses")
def create_course(course: Course):
    # Kiểm tra xem code hoặc id có bị trùng với khóa học cũ không
    for c in courses:
        if c["code"] == course.code:
            raise HTTPException(status_code=400, detail="Mã code đã bị trùng")
        if c["id"] == course.id:
            raise HTTPException(status_code=400, detail="ID đã bị trùng")
            
    # Lệnh append dùng để nhét thêm đồ mới vào List
    courses.append(course.dict())
    return {"message": "Thêm thành công"}


# --- SỬA KHÓA HỌC ---
@app.put("/courses/{course_id}")
def update_course(course_id: int, course: Course):
    # Kiểm tra xem code mới sửa có vô tình trùng với khóa khác không
    for c in courses:
        if c["code"] == course.code and c["id"] != course_id:
            raise HTTPException(status_code=400, detail="Mã code trùng với khóa khác")

    # Dùng vòng lặp đếm số thứ tự (i) để sửa trực tiếp trong List
    for i in range(len(courses)):
        if courses[i]["id"] == course_id:
            courses[i]["code"] = course.code
            courses[i]["name"] = course.name
            courses[i]["duration"] = course.duration
            courses[i]["fee"] = course.fee
            return {"message": "Sửa thành công", "data": courses[i]}
            
    raise HTTPException(status_code=404, detail="Course not found")


# --- XÓA KHÓA HỌC ---
@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    # Tìm vị trí (i) của khóa học cần xóa
    for i in range(len(courses)):
        if courses[i]["id"] == course_id:
            # Lệnh pop(i) dùng để rút một món đồ khỏi List tại vị trí thứ i
            courses.pop(i)
            return {"message": "Xóa thành công"}
            
    raise HTTPException(status_code=404, detail="Course not found")