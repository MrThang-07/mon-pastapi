"""
===================================================================
PHẦN 1: PHÁT HIỆN LỖI (BUG DETECTION)
===================================================================
1. Lỗi điều kiện phân quyền trong require_admin():
   - Dòng code lỗi: if current_user["role"] == "admin" or current_user["is_active"]:
   - Giải thích: Dùng toán tử `or` khiến BẤT KỲ tài khoản nào đang hoạt động 
     (is_active=True) đều vượt qua được bước kiểm tra Admin.
   - Test case 1: Dùng `user-token` gọi DELETE /admin/courses/1. 
     Mong đợi: 403. Thực tế: 200 OK.

2. Lỗi Middleware yêu cầu Authorization với mọi request & chặn OPTIONS:
   - Dòng code lỗi: if "authorization" not in request.headers: return 401
   - Giải thích: Middleware bắt ép mọi request phải có token. Điều này vô tình chặn 
     luôn API công khai (/health) và các request OPTIONS (CORS preflight của trình duyệt).
   - Test case 2: Gọi GET /health. Mong đợi: 200. Thực tế: 401.
   - Test case 3: Gọi OPTIONS /courses. Mong đợi: Pass. Thực tế: 401.

3. Lỗi cấu hình CORS quá dễ dãi:
   - Dòng code lỗi: allow_origins=["*"]
   - Giải thích: Cho phép mọi trang web gọi API, vi phạm quy tắc chỉ cho phép 2 frontend cụ thể.
   - Test case 4: Origin: https://unknown-website.com gọi API. 
     Mong đợi: Bị CORS chặn. Thực tế: Vẫn pass.

4. Lỗi thiếu kiểm tra tài khoản bị khóa trong get_current_user():
   - Tài khoản `locked01` (is_active: False) vẫn có thể truy cập API.
===================================================================
PHẦN 2: SỬA SOURCE CODE (Bên dưới)
===================================================================
"""

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# [VÁ LỖI 1]: Sửa cấu hình CORS, chỉ định đích danh 2 URL Frontend được phép
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

TOKENS = {
    "admin-token": {
        "username": "admin01",
        "role": "admin",
        "is_active": True,
    },
    "user-token": {
        "username": "student01",
        "role": "user",
        "is_active": True,
    },
    "locked-token": {
        "username": "locked01",
        "role": "user",
        "is_active": False,
    },
}


@app.middleware("http")
async def custom_middleware(request, call_next):
    # [VÁ LỖI 2]: Xóa bỏ logic kiểm tra cứng "authorization" ở Middleware.
    # Xác thực token sẽ do OAuth2PasswordBearer và Dependencies đảm nhận.
    # Việc này giúp API /health và CORS preflight (OPTIONS) đi qua bình thường.
    
    response = await call_next(request)
    response.headers["X-System-Name"] = "Learning Management System"
    return response


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = TOKENS.get(token)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
        
    # [VÁ LỖI 4]: Chặn tài khoản bị khóa (is_active = False) truy cập hệ thống
    if not user.get("is_active"):
        raise HTTPException(
            status_code=403,
            detail="Inactive user",
        )

    return user


def require_admin(current_user: dict = Depends(get_current_user)):
    # [VÁ LỖI 3]: Sửa toán tử 'or' thành kiểm tra chính xác role == "admin".
    # (Hàm get_current_user ở trên đã lo việc kiểm tra is_active rồi).
    if current_user.get("role") == "admin":
        return current_user

    raise HTTPException(
        status_code=403,
        detail="Admin permission required",
    )


@app.get("/health")
def health_check():
    # Giờ đây /health đã được công khai hoàn toàn
    return {"status": "UP"}


@app.get("/courses")
def get_courses(current_user: dict = Depends(get_current_user)):
    return {
        "items": [
            {"id": 1, "name": "FastAPI Basic"},
            {"id": 2, "name": "FastAPI Security"},
        ]
    }


@app.delete("/admin/courses/{course_id}")
def delete_course(
    course_id: int,
    current_user: dict = Depends(require_admin), # Sử dụng require_admin ở đây
):
    return {
        "message": f"Course {course_id} has been deleted",
        "deleted_by": current_user["username"],
    }