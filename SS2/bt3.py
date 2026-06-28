# Phần 1: Báo cáo phân tích (Analysis Report)
# 1. Input của bài toán là gì?
# Danh sách (List) gồm các Object/Dict chứa thông tin của toàn bộ sinh viên trong hệ thống (id, name, status).

# 2. Output mong muốn là gì?
# Một JSON Object có cấu trúc chuẩn hóa gồm 2 trường chính:

# message: Chuỗi thông báo trạng thái kết quả.

# data: Mảng (Array/List) chứa danh sách các sinh viên thỏa mãn điều kiện lọc.

# 3. Điều kiện dùng để xác định sinh viên đang học?
# Trường status của sinh viên đó phải có giá trị chính xác là chuỗi "active" (status == "active").

# 4. Các bước xử lý API GET /students/active
# Bước 1: Tiếp nhận HTTP Request GET từ Client gửi tới endpoint /students/active.

# Bước 2: Khởi tạo một danh sách rỗng (ví dụ: active_students = []) để lưu trữ kết quả lọc.

# Bước 3: Duyệt qua từng sinh viên trong danh sách students tổng bằng vòng lặp. Nếu sinh viên nào có status == "active", tiến hành thêm (append) sinh viên đó vào danh sách active_students.

# Bước 4: Kiểm tra độ dài của danh sách kết quả (active_students):

# Nếu danh sách rỗng (độ dài bằng 0): Trả về JSON chứa message: "Không có sinh viên đang học" và data: [].

# Nếu danh sách có dữ liệu: Trả về JSON chứa message: "Danh sách sinh viên đang học" và data: active_students.
# Phàn 2 : sửa code :
from fastapi import FastAPI

app = FastAPI()

# Giả lập database danh sách sinh viên ban đầu
students = [
    {"id": 1, "name": "An", "status": "active"},
    {"id": 2, "name": "Binh", "status": "inactive"},
    {"id": 3, "name": "Cuong", "status": "active"},
    {"id": 4, "name": "Dung", "status": "pending"}
]

# Định nghĩa API endpoint theo đúng yêu cầu: GET /students/active
@app.get("/students/active")
def get_active_students():
    # Bước 1: Dùng list comprehension để lọc nhanh các sinh viên có status là active
    active_students = [student for student in students if student["status"] == "active"]
    
    # Bước 2: Kiểm tra bẫy dữ liệu và ràng buộc đầu ra
    if not active_students:
        return {
            "message": "Không có sinh viên đang học",
            "data": []
        }
        
    # Bước 3: Trả về cấu trúc thành công đúng mong đợi
    return {
        "message": "Danh sách sinh viên đang học",
        "data": active_students
    }