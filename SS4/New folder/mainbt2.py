# ==========================================
# PHẦN 1: PHÂN TÍCH LỖI (BÀI TẬP VẬN DỤNG 2)
# ==========================================
# 1. Endpoint hiện tại có Path Parameter không?
#    - Có, endpoint hiện tại đã khai báo chính xác cấu trúc Path Parameter.
#
# 2. Path Parameter trong bài này là gì?
#    - Là `{status}` nằm trên URL.
#
# 3. Khi gọi "/orders/status/pending", biến `status` nhận giá trị gì?
#    - Biến `status` trong hàm sẽ nhận giá trị là chuỗi ký tự (string): "pending".
#
# 4. Vì sao API hiện tại trả về sai dữ liệu?
#    - Vì hàm xử lý nhận giá trị `status` từ URL về nhưng bỏ không, hoàn toàn không sử dụng 
#      để lọc (filter) danh sách đơn hàng mà lại trực tiếp trả về toàn bộ mảng `orders`.
#
# 5. Dòng code khiến API bỏ qua giá trị `status`:
#    - return orders
# ==========================================

from fastapi import FastAPI

app = FastAPI()

# Danh sách đơn hàng giả lập
orders = [
    {"id": 1, "customer_name": "Nguyễn Văn An", "total": 250000, "status": "pending"},
    {"id": 2, "customer_name": "Trần Thị Bình", "total": 500000, "status": "paid"},
    {"id": 3, "customer_name": "Lê Văn Cường", "total": 150000, "status": "cancelled"},
    {"id": 4, "customer_name": "Phạm Thị Dung", "total": 320000, "status": "pending"}
]

# Các trạng thái hợp lệ theo nghiệp vụ hệ thống
VALID_STATUSES = ["pending", "paid", "cancelled"]

# PHẦN 2: SOURCE CODE ĐÃ SỬA LỖI
@app.get("/orders/status/{status}")
def get_orders_by_status(status: str):
    # Bước 1: Kiểm tra trạng thái truyền vào có hợp lệ hay không
    if status not in VALID_STATUSES:
        return {"message": "Trạng thái đơn hàng không hợp lệ"}
        
    # Bước 2: Lọc danh sách đơn hàng có status trùng với tham số truyền vào
    filtered_orders = []
    for order in orders:
        if order["status"] == status:
            filtered_orders.append(order)
            
    # Bước 3: Trả về danh sách đơn hàng đã được lọc
    return filtered_orders