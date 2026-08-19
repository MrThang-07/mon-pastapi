from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ==========================================
# PHẦN 4: CẤU HÌNH CORS NGHIÊM NGẶT
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://internal.megamart.com"], # Chỉ cho phép domain này
    allow_credentials=True,
    allow_methods=["GET", "POST"],                   # Chỉ cho phép GET, POST
    allow_headers=["Content-Type", "X-User-Role"],   # Chỉ cho phép các Header này
)

# ==========================================
# PHẦN 1 & 2: HỆ THỐNG VAI TRÒ & MIDDLEWARE PHÂN QUYỀN
# ==========================================
# Hàm này đóng vai trò như một Custom Middleware cho từng Route
def role_checker(allowed_roles: list[str]):
    def verify_role(x_user_role: str = Header(None)):
        # Nếu không truyền Header X-User-Role
        if not x_user_role:
            raise HTTPException(status_code=403, detail="Permission Denied")
        
        # Nếu Role truyền lên không nằm trong danh sách được phép
        if x_user_role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Permission Denied")
        
        # Hợp lệ -> Cho đi tiếp
        return x_user_role
    
    return verify_role

# ==========================================
# PHẦN 3: CÁC API ENDPOINT THỬ NGHIỆM
# ==========================================

# 1. Chỉ ADMIN và HR được truy cập
@app.get("/api/v1/salary/modify", dependencies=[Depends(role_checker(["ADMIN", "HR"]))])
def modify_salary():
    return {"message": "Thành công: Bạn đang xem/sửa bảng lương."}

# 2. Chỉ duy nhất ADMIN được truy cập
@app.get("/api/v1/system/settings", dependencies=[Depends(role_checker(["ADMIN"]))])
def system_settings():
    return {"message": "Thành công: Bạn đang truy cập cấu hình hệ thống."}

# 3. Cả ADMIN, HR, STAFF đều được truy cập
@app.get("/api/v1/profile", dependencies=[Depends(role_checker(["ADMIN", "HR", "STAFF"]))])
def view_profile():
    return {"message": "Thành công: Bạn đang xem hồ sơ cá nhân."}