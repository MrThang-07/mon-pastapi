
# =========================================================================================
# 5. YÊU CẦU ĐẦU RA - CHỈ RA LỖI BẰNG TEST CASE 
# =========================================================================================
# STT | Dữ liệu gửi lên | Kết quả hiện tại (Mã HTTP + Body)        | Kết quả đúng mong muốn                 | Lỗi phát hiện
# ----------------------------------------------------------------------------------------------------------------------------------
# 1   | order_id = 999  | Mã HTTP: 200 OK                          | Mã HTTP: 404 Not Found                 | Trả về sai mã trạng thái 
#     |                 | Body: {"message": "Order not found"}     | Body: {"detail": "Không tìm thấy"}     | (200 thay vì 404) khi 
#     |                 |                                          |                                        | không tìm thấy dữ liệu.
# ----------------------------------------------------------------------------------------------------------------------------------
# 2   | order_id = 1    | Mã HTTP: 200 OK                          | Mã HTTP: 200 OK                        | Lộ dữ liệu nhạy cảm 
#     |                 | Body: {"id": 1,                          | Body: {"id": 1,                        | của hệ thống nội bộ
#     |                 | "customer_name": "Nguyen Van A",         | "customer_name": "Nguyen Van A",       | (profit_margin và 
#     |                 | "total_amount": 1500000.0,               | "total_amount": 1500000.0}             | supplier_id).
#     |                 | "profit_margin": 0.25,                   |                                        |
#     |                 | "supplier_id": "SUP_DELL_01"}            |                                        |
# =========================================================================================

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# Dữ liệu nội bộ trong bộ nhớ tạm - Chứa các trường nhạy cảm
orders_db = [
    {
        "id": 1,
        "customer_name": "Nguyen Van A",
        "total_amount": 1500000.0,
        "profit_margin": 0.25,      # Nhạy cảm - Cấm lộ!
        "supplier_id": "SUP_DELL_01" # Nhạy cảm - Cấm lộ!
    },
    {
        "id": 2,
        "customer_name": "Tran Thi B",
        "total_amount": 350000.0,
        "profit_margin": 0.30,       # Nhạy cảm - Cấm lộ!
        "supplier_id": "SUP_LOGI_02"  # Nhạy cảm - Cấm lộ!
    }
]

class OrderInternal(BaseModel):
    id: int
    customer_name: str
    total_amount: float
    profit_margin: float
    supplier_id: str

# Schema cho API Public - Đã loại bỏ các trường nhạy cảm
class get_baomat(BaseModel):
    id: int
    customer_name: str
    total_amount: float

@app.get("/orders/{order_id}", status_code=status.HTTP_200_OK, response_model=get_baomat)
def get_order_detail(order_id: int):
    for order in orders_db:
        if order["id"] == order_id:
            return order 
            
    # Trả về chuẩn mã lỗi 404 khi không tìm thấy
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Không tìm thấy"
    )