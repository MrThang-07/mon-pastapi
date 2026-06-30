# =====================================================================
# PHẦN 1: PHÂN TÍCH & ĐỀ XUẤT ĐA GIẢI PHÁP
# =====================================================================
# 1. Phân tích yêu cầu Input / Output:
#    - Input: Dữ liệu học viên gửi lên qua Request Body dạng JSON gồm:
#      full_name (str), email (str), age (int), course (str), phone (str).
#    - Output thành công: Trả về thông tin học viên vừa được thêm kèm mã ID mới.
#    - Output thất bại: Trả về thông báo lỗi cụ thể (thiếu trường, sai định dạng, trùng email).
#
# 2. Đề xuất 2 giải pháp validate dữ liệu:
#    - Giải pháp 1: Validate thủ công bằng câu lệnh IF/ELSE trong hàm (Basic Python).
#    - Giải pháp 2: Validate tự động bằng Pydantic Model (Tính năng có sẵn của FastAPI).
#
# =====================================================================
# PHẦN 2: SO SÁNH & LỰA CHỌN
# =====================================================================
# 1. Bảng so sánh các giải pháp:
#    +------------------+---------------------------+---------------------------+
#    | Tiêu chí         | Giải pháp 1 (IF/ELSE)     | Giải pháp 2 (Pydantic)    |
#    +------------------+---------------------------+---------------------------+
#    | Độ dễ hiểu       | Rất dễ hiểu, dùng logic   | Cần học thêm cú pháp      |
#    |                  | Python căn bản.           | của lớp đối tượng (Class).|
#    +------------------+---------------------------+---------------------------+
#    | Số lượng code    | Viết nhiều, mỗi quy tắc   | Viết ít, định nghĩa kiểu  |
#    | cần viết         | là một câu điều kiện IF.  | dữ liệu một lần ở Model.  |
#    +------------------+---------------------------+---------------------------+
#    | Khả năng kiểm    | Thủ công, dễ sót nếu có   | Tự động bắt lỗi thiếu     |
#    | soát lỗi         | nhiều trường dữ liệu.     | trường, sai kiểu dữ liệu. |
#    +------------------+---------------------------+---------------------------+
#    | Độ rõ ràng của   | Thấp, dữ liệu nhận vào    | Cao, nhìn vào Model biết  |
#    | cấu trúc dữ liệu | chỉ là các biến rời rạc.  | ngay cấu trúc JSON.       |
#    +------------------+---------------------------+---------------------------+
#
# 2. Chốt lựa chọn giải pháp:
#    - Lựa chọn: Giải pháp 2 (Sử dụng Pydantic Model).
#    - Lý do: Đây là giải pháp chuẩn chỉnh của FastAPI. Giúp tự động kiểm tra lỗi thiếu trường 
#      hoặc sai kiểu dữ liệu ngay từ "vòng gửi xe" mà không cần viết nhiều câu lệnh IF/ELSE dài dòng.
#
# =====================================================================
# PHẦN 3: THIẾT KẾ & TRIỂN KHAI (SOURCE CODE)
# =====================================================================

from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

# 1. KHỞI TẠO PYDANTIC MODEL ĐỂ VALIDATE TỰ ĐỘNG
class StudentCreate(BaseModel):
    # Quy tắc 1: full_name bắt buộc (str), không trống và độ dài tối thiểu là 3 ký tự
    full_name: str = Field(..., min_length=3)
    
    # Quy tắc 2: email bắt buộc và phải đúng định dạng email (dùng EmailStr)
    email: EmailStr
    
    # Các trường còn lại với kiểu dữ liệu tương ứng (nếu không truyền sẽ báo lỗi kiểu dữ liệu)
    age: int
    course: str
    phone: str


# Danh sách học viên giả lập (Database tạm thời)
students_db = [
    {
        "id": 1, 
        "full_name": "Nguyen Van B", 
        "email": "existing@gmail.com", 
        "age": 22, 
        "course": "python", 
        "phone": "0123456789"
    }
]


# 2. API ĐĂNG KÝ HỌC VIÊN
@app.post("/students")
def create_student(student: StudentCreate): # Sử dụng Model vừa tạo làm kiểu dữ liệu đầu vào
    

    # Kiểm tra quy tắc nghiệp vụ còn lại: Email đã tồn tại (Cần check thủ công trong DB)
    for existing_student in students_db:
        if existing_student["email"] == student.email:
            return {"detail": "Email đã tồn tại trong hệ thống"}

    # Nếu tất cả đều hợp lệ, tiến hành lưu trữ dữ liệu
    new_id = len(students_db) + 1
    
    # Chuyển đổi object Pydantic thành dictionary của Python để dễ lưu trữ
    new_student_data = student.model_dump()
    new_student_data["id"] = new_id

    # Thêm vào database giả lập
    students_db.append(new_student_data)
    
    # Trả về kết quả thành công cho Client
    return {
        "message": "Thêm học viên thành công",
        "student": new_student_data
    }