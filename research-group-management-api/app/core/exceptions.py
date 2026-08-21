from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from datetime import datetime

# Hàm nhỏ lấy giờ cho gọn code
def lay_gio_hien_tai():
    return datetime.now().isoformat()

def setup_exception_handlers(app: FastAPI):
    
    # 1. Bắt các lỗi cơ bản theo yêu cầu (400, 403, 404...)
    @app.exception_handler(HTTPException)
    async def bat_loi_http_co_ban(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "code": exc.status_code,
                "error": "Lỗi HTTP",
                "message": exc.detail,
                "data": None,
                "timestamp": lay_gio_hien_tai()
            }
        )

    # 2. Bắt lỗi 422 (Lỗi Validate form từ Pydantic Schemas)
    @app.exception_handler(RequestValidationError)
    async def bat_loi_nhap_lieu_422(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "code": 422,
                "error": "Lỗi Nhập Liệu",
                "message": "Dữ liệu bạn nhập không hợp lệ, vui lòng kiểm tra lại!",
                "data": exc.errors(), # Trả về mảng lỗi để Frontend bôi đỏ ô input
                "timestamp": lay_gio_hien_tai()
            }
        )
    