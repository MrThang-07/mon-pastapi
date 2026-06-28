# Phần 1: Phân tích Input/Output
# Input của bài toán: Danh sách các cuốn sách (Mảng các Object/Dict) chứa thông tin: mã sách (id), tên sách (title), và số lượng tồn kho (quantity). Dữ liệu thực tế có thể chứa bẫy: thiếu trường quantity hoặc quantity có giá trị âm.

# Output mong muốn: Một Object JSON chuẩn hóa cấu trúc gồm:
# message (string): Thông báo trạng thái kết quả trả về.
# data (list): Danh sách các sách thỏa mãn điều kiện lọc sắp hết hàng và hợp lệ.
# Điều kiện để xác định sách sắp hết hàng: Quyển sách phải có trường quantity hợp lệ (không thiếu, không âm) và giá trị thỏa mãn: $quantity \le 5$.
# Phần 2: Đề xuất giải pháp duyệt và lọc sách
# Giải pháp 1: Sử dụng vòng lặp for truyền thống kết hợp câu lệnh điều kiện if-elif-else
# Duyệt qua từng phần tử trong danh sách sách bằng vòng lặp for.Dùng phương thức .get("quantity") hoặc toán tử in để check bẫy dữ liệu (thiếu trường hoặc số lượng < 0) và dùng continue để bỏ qua.Nếu thỏa mãn điều kiện $\le 5$, dùng phương thức .append() đưa vào mảng kết quả.
# Giải pháp 2: Sử dụng List Comprehension viết gọn kết hợp hàm bổ trợ (Helper Function)
# Viết một hàm riêng biệt is_low_stock(book) trả về kiểu Boolean (True/False) để bao bọc toàn bộ logic kiểm tra bẫy dữ liệu và điều kiện số lượng.

# Sau đó, dùng cú pháp rút gọn List Comprehension để lọc danh sách sách chỉ trong 1 dòng code dựa trên hàm bổ trợ đó.
# Phần 4: Thiết kế các bước xử lý
# Khởi tạo: Khai báo ứng dụng FastAPI (app = FastAPI()).

# Mock Data: Khai báo danh sách dữ liệu books chứa đầy đủ các case (hợp lệ, sắp hết hàng, thiếu trường, giá trị âm).

# Cấu hình Route: Tạo endpoint định tuyến @app.get("/books/low-stock").

# Xử lý logic lọc:

# Tạo mảng rỗng low_stock_books = [].

# Chạy vòng lặp for book in books.

# Bẫy 1: Kiểm tra nếu "quantity" not in book, bỏ qua (continue).

# Bẫy 2: Kiểm tra nếu book["quantity"] < 0, bỏ qua (continue).

# Lọc điều kiện: Nếu book["quantity"] <= 5, thêm vào mảng: low_stock_books.append(book).

# Kiểm tra kết quả đầu ra:

# Nếu mảng low_stock_books rỗng: Trả về Object gồm message báo không có và data là [].

# Nếu có dữ liệu: Trả về message thành công kèm data chứa danh sách vừa lọc.
# Phần 5: Triển khai code
from fastapi import FastAPI

app = FastAPI()

books = [
    {"id": 1, "title": "Python Basic", "quantity": 12},
    {"id": 2, "title": "FastAPI Beginner", "quantity": 3},
    {"id": 3, "title": "Clean Code", "quantity": 5},
    {"id": 4, "title": "Database Design", "quantity": 0},
    {"id": 5, "title": "Web API Design", "quantity": 20},
    {"id": 6, "title": "Java Basic"},
    {"id": 7, "title": "Spring Boot", "quantity": -2}
]

@app.get("/books/low-stock")
def get_low_stock_books():
    low_stock_books = []
    
    for book in books:
        if "quantity" not in book:
            continue
            
        if book["quantity"] < 0:
            continue
            
        if book["quantity"] <= 5:
            low_stock_books.append(book)
            
    if not low_stock_books:
        return {
            "message": "Không có sách nào sắp hết hàng",
            "data": []
        }
        
    return {
        "message": "Danh sách sách sắp hết hàng",
        "data": low_stock_books
    }