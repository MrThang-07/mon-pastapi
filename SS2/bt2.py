# Phần 1: Phân tích lỗi (Analysis)
# 1. Endpoint hiện tại trong source code là gì?
# Endpoint hiện tại trong mã nguồn là: GET /student (được khai báo ở dòng số 9: @app.get("/student")).

# 2. Vì sao khi gọi GET /students lại bị lỗi 404 Not Found?
# Vì trong mã nguồn hiện tại, hàm get_student() chỉ được định tuyến (routing) cho đường dẫn /student (số ít). FastAPI không tìm thấy bất kỳ route nào cấu hình cho đường dẫn /students (số nhiều), do đó hệ thống tự động trả về lỗi 404 Not Found.

# 3. Vì sao tên endpoint /student chưa phù hợp với yêu cầu lấy danh sách sinh viên?
# Theo chuẩn thiết kế RESTful API, đường dẫn đại diện cho một tập hợp danh sách dữ liệu (Collection Resource) phải sử dụng danh từ số nhiều (/students).

# Việc đặt tên là /student (số ít) thường ám chỉ việc thao tác với một sinh viên cụ thể (ví dụ: lấy chi tiết một sinh viên theo ID dạng /students/{id}), không đúng với ý nghĩa nghiệp vụ là "lấy toàn bộ danh sách".

# 4. Vì sao dòng return students[0] chưa đúng với yêu cầu nghiệp vụ?
# Cú pháp students[0] trong Python dùng để truy cập vào phần tử đầu tiên của danh sách (index = 0), cụ thể ở đây là {"id": 1, "name": "An"}.

# Bối cảnh nghiệp vụ yêu cầu API phải trả về toàn bộ danh sách sinh viên (cả 3 người An, Bình, Cường), việc chỉ trả về phần tử đầu tiên đã làm sai hoàn toàn logic yêu cầu.

# 5. API đúng theo yêu cầu khách hàng nên có đường dẫn là gì?
# Đường dẫn đúng chuẩn theo yêu cầu của khách hàng và nghiệp vụ phải là: GET /students
# Phần 2 : sửa code 
from fastapi import FastAPI

app = FastAPI()

# Danh sách dữ liệu sinh viên giả lập
students = [
    {"id": 1, "name": "An"},
    {"id": 2, "name": "Binh"},
    {"id": 3, "name": "Cuong"},
]

# 1. Sửa endpoint đúng là /students (số nhiều)
@app.get("/students")
# 2. Đổi tên hàm rõ nghĩa là get_students
def get_students():
    # 3. Trả về toàn bộ danh sách sinh viên
    return students