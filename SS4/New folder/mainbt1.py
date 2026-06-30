# ==========================================
# PHẦN 1: PHÂN TÍCH LỖI (BÀI TẬP VẬN DỤNG 1)
# ==========================================
# 1. Vì sao API trả về 404 Not Found?
#    - Vì FastAPI hiểu "/products/product_id" là một đường dẫn tĩnh (fixed path) cố định.
#    - Khi gọi "/products/1", hệ thống không tìm thấy route nào khớp chính xác nên báo 404.
#
# 2. Dòng code khai báo sai:
#    - @app.get("/products/product_id")
#
# 3. Vì sao không phải là Path Parameter?
#    - Thiếu cặp dấu ngoặc nhọn `{}`. Trong FastAPI, mọi biến trên URL bắt buộc phải bọc trong `{}`.
#
# 4. Endpoint đúng sau khi sửa:
#    - @app.get("/products/{product_id}")
# ==========================================

from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop Dell", "price": 15000000},
    {"id": 2, "name": "Chuột Logitech", "price": 350000},
    {"id": 3, "name": "Bàn phím cơ", "price": 1200000}
]

# PHẦN 2: SOURCE CODE ĐÃ SỬA
@app.get("/products/{product_id}")
def get_product_detail(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    return {"message": "Không tìm thấy sản phẩm"}