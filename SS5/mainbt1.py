from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Laptop Dell", "price": 15000000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse Logitech", "price": 350000, "stock": 50}
]

class ProductCreate(BaseModel):
    code: str
    name: str
    price: float
    stock: int

# ==============================================================================
# PHÂN TÍCH LỖI LOGIC CỦA CODE CŨ:
# 1. Thiếu bước validate (kiểm tra) trùng mã 'code' trước khi nạp dữ liệu vào list.
# 2. Trả về HTTP Status mặc định là 200 OK thay vì chuẩn 201 Created khi tạo mới.
# ==============================================================================

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    
    # HÀM SỬA: Quét danh sách để kiểm tra trùng mã sản phẩm
    for p in products:
        if p.get("code") == product.code:
            # Ngắt xử lý và báo lỗi ngay lập tức nếu phát hiện trùng mã
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Ma san pham '{product.code}' da ton tai trong he thong!"
            )
            
    # Tiến hành tạo mới khi dữ liệu hợp lệ
    new_product = {
        "id": len(products) + 1,
        "code": product.code,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }
    
    products.append(new_product)
    return {
        "message": "Create product successfully",
        "data": new_product
    }