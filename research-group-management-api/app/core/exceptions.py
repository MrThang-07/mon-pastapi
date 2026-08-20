from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from datetime import datetime

# Hàm nhỏ để lấy giờ hiện tại cho gọn
def lay_gio_hien_tai():
    return datetime.now().isoformat()

def setup_exception_handlers(app: FastAPI):
    
    # BẪY 1: Lỗi thông thường (VD: 404 Không tìm thấy, 403 Cấm truy cập)
    @app.exception_handler(HTTPException)
    async def bat_loi_http(request: Request, exc: HTTPException):
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

    # BẪY 2: Lỗi nhập liệu (VD: 422 Nhập thiếu Email, Pass quá ngắn)
    @app.exception_handler(RequestValidationError)
    async def bat_loi_nhap_lieu(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "code": 422,
                "error": "Lỗi Nhập Liệu",
                "message": "Dữ liệu bạn nhập không hợp lệ, vui lòng kiểm tra lại!",
                "data": exc.errors(),      
                "timestamp": lay_gio_hien_tai()
            }
        )

    # BẪY 3: Lỗi hệ thống sập (VD: 500 Code sai, rớt mạng Database)
    @app.exception_handler(Exception)
    async def bat_loi_server_sap(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "code": 500,
                "error": "Lỗi Máy Chủ",
                "message": "Hệ thống đang gặp sự cố, vui lòng thử lại sau!",
                "data": str(exc),         
                "timestamp": lay_gio_hien_tai()
            }
        )