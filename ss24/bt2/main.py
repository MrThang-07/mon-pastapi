from fastapi import FastAPI, Header, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ==========================================
# PHẦN 4: CẤU HÌNH CORS ĐA DOMAIN (WHITELIST)
# ==========================================
# Chỉ cho phép các domain chính thức của FlashMove
ALLOWED_ORIGINS = [
    "https://driver.flashmove.io",
    "https://hub.flashmove.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,                   # Chặn toàn bộ domain lạ, chỉ cho phép 2 domain trên
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],          # Chỉ cho phép các Method an toàn/cần thiết
    allow_headers=["Content-Type", "X-Role-Identity"], # Khai báo Header hợp lệ
)

# ==========================================
# PHẦN 1 & 2: HỆ THỐNG VAI TRÒ & MIDDLEWARE PHÂN QUYỀN
# ==========================================

# 1. Tạo một Custom Exception để xử lý lỗi 403 theo đúng định dạng JSON yêu cầu
class UnauthorizedRoleException(Exception):
    pass

@app.exception_handler(UnauthorizedRoleException)
async def unauthorized_role_handler(request: Request, exc: UnauthorizedRoleException):
    return JSONResponse(
        status_code=403,
        content={"status": "Rejected", "reason": "Unauthorized action for this role"}
    )

# 2. Hàm Dependency đóng vai trò làm Middleware phân quyền
def role_checker(allowed_roles: list[str]):
    def verify_role(x_role_identity: str = Header(None)):
        # Bóc tách và kiểm tra Header X-Role-Identity
        if not x_role_identity or x_role_identity not in allowed_roles:
            # Nếu không có header hoặc vai trò không hợp lệ -> ném ra lỗi đã cấu hình ở trên
            raise UnauthorizedRoleException()
        
        # Nếu hợp lệ -> Cho phép Request đi tiếp
        return x_role_identity
    
    return verify_role

# ==========================================
# PHẦN 3: CÁC API ENDPOINT THỰC NGHIỆM
# ==========================================

# 1. Gán đơn hàng: Chỉ duy nhất DISPATCHER
@app.post("/api/v1/orders/assign", dependencies=[Depends(role_checker(["DISPATCHER"]))])
def assign_order():
    return {"message": "Thành công: Đã gán đơn hàng cho tài xế."}

# 2. Cập nhật trạng thái: DISPATCHER và DRIVER
@app.patch("/api/v1/orders/status", dependencies=[Depends(role_checker(["DISPATCHER", "DRIVER"]))])
def update_order_status():
    return {"message": "Thành công: Đã cập nhật trạng thái đơn hàng."}

# 3. Xem tiến trình: Tất cả các vai trò
@app.get("/api/v1/orders/track", dependencies=[Depends(role_checker(["DISPATCHER", "DRIVER", "CUSTOMER_SUPPORT"]))])
def track_order():
    return {"message": "Thành công: Đang theo dõi tiến trình đơn hàng."}