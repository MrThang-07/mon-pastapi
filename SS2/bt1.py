# Phần 1: Phân tích lỗi
# 1. Trace luồng xử lý khi gọi /getStudents
# Bước 1: Client (Frontend/Tester) gửi một HTTP request với phương thức GET đến endpoint /getStudents.

# Bước 2: FastAPI nhận request và định tuyến (route) đến hàm xử lý get_students().

# Bước 3: Tại đây, hệ thống lấy danh sách students = ["An", "Binh", "Cuong"]. Thay vì trả về mảng này, hàm lại thực hiện ép kiểu sang chuỗi bằng str(students) rồi cộng chuỗi với đoạn văn bản phía trước.

# Bước 4: Hàm trả về một chuỗi Plain Text duy nhất: "Danh sach sinh vien: ['An', 'Binh', 'Cuong']".
# 2. Lý do FastAPI không nên trả về String trong API JSON
# Khó khăn cho Frontend: Định dạng JSON sinh ra để máy tính có thể dễ dàng đọc và phân tách dữ liệu (parse). Khi trả về một chuỗi gom tất cả lại như trên, Frontend không thể dùng các hàm lặp (như .map() trong JavaScript) để hiển thị danh sách lên giao diện. Họ sẽ phải viết thêm code để cắt chuỗi rất phức tạp và dễ lỗi.

# Đi ngược lại thế mạnh của FastAPI: FastAPI hỗ trợ tự động chuyển đổi (serialize) các kiểu dữ liệu của Python như list, dict, Pydantic model thành JSON chuẩn hóa. Việc ép kiểu sang str đã vô tình phá vỡ tính năng tự động này.

# 3. Lỗi trong thiết kế REST endpoint (Naming Convention)
# Sử dụng động từ trong đường dẫn: Endpoint đang đặt tên là /getStudents. Theo chuẩn RESTful API, đường dẫn nên đại diện cho một tài nguyên (Resource) và sử dụng danh từ, không sử dụng động từ (get, post, delete...). Bản thân phương thức HTTP GET đã mang ý nghĩa là "lấy dữ liệu" rồi.

# Sai quy cách đặt tên: Sử dụng CamelCase (/getStudents) thay vì viết thường toàn bộ hoặc dùng dấu gạch ngang (kebab-case). Đối với danh sách tập hợp, ta nên dùng danh từ số nhiều (Plural).
# Phần 2: Sửa code :
from fastapi import FastAPI

app = FastAPI()
students = ["An", "Binh", "Cuong"]
@app.get("/students")
def get_students():
    return students