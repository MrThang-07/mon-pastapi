
# ==============================================================================================================
# 5. YÊU CẦU ĐẦU RA - CHỈ RA LỖI BẰNG TEST CASE (DỰA TRÊN MÃ NGUỒN CŨ LỖI)
# ==============================================================================================================
# STT | Dữ liệu gửi lên                     | Kết quả hiện tại (Mã HTTP + Body)      | Kết quả đúng mong muốn             | Lỗi phát hiện
# ----------------------------------------------------------------------------------------------------------------------
# 1   | PUT /orders/999/status với          | Mã HTTP: 200 OK                        | Mã HTTP: 404 Not Found             | Lọt luồng xử lý lỗi. Trạng thái 
#     | status="SHIPPING"                   | Body: {"statusCode": 200,              | Body: {"detail": "Không tồn tại"}  | trả về 200 OK thay vì 404 Not Found 
#     |                                     | "message": "Cập nhật thành công",      |                                    | khi không tìm thấy đơn hàng.
#     |                                     | "data": null}                          |                                    | 
# ----------------------------------------------------------------------------------------------------------------------
# 2   | PUT /orders/1/status với            | Mã HTTP: 200 OK                        | Mã HTTP: 400 Bad Request           | Xử lý sai HTTP Status. API trả về
#     | status="TRONG_SANG"                 | Body: {"error": "Trạng thái            | Body: {"detail": "Sai trạng thái"} | 200 OK thay vì báo lỗi 400 (hoặc 422)
#     |                                     | không hợp lệ"}                         |                                    | khi dữ liệu đầu vào không hợp lệ.
# ==============================================================================================================


from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

orders_db = [
    {"id": 1, "customer_name": "Nguyen Van A", "status": "PENDING"},
    {"id": 2, "customer_name": "Tran Thi B", "status": "SHIPPING"}
]

class StatusUpdate(BaseModel):
    status: str

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    return next((o for o in orders_db if o["id"] == order_id), None)

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, data: StatusUpdate):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    
    # 1. Chặn lỗi không tìm thấy đơn hàng (Raise sẽ làm dừng ngay luồng chạy)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tồn tại"
        )
        
    # 2. Chặn lỗi trạng thái không hợp lệ
    if data.status not in ["PENDING", "SHIPPING", "DELIVERED"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sai trạng thái"
        )
        
    # 3. Code chỉ chạy được đến đây khi các dữ liệu đều đã hợp lệ
    order["status"] = data.status

    return {"statusCode": 200, "message": "Cập nhật thành công", "data": order}