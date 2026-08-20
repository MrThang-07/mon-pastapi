from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from datetime import datetime

def setup_exception_handlers(app: FastAPI):
    
    # 1. Bắt các lỗi HTTP thông thường (404, 401, 403...)
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "code": exc.status_code,
                "error": "HTTP Error",
                "message": exc.detail,
                "data": None,  # Không có dữ liệu chi tiết thì để null
                "timestamp": datetime.now().isoformat()
            }
        )

    # 2. Bắt lỗi 422 - Validate dữ liệu 
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "code": 422,
                "error": "Validation Error",
                "message": "Dữ liệu đầu vào không hợp lệ",
                "data": exc.errors(), 
                "timestamp": datetime.now().isoformat()
            }
        )

    # 3. Bắt lỗi hệ thống 500
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "code": 500,
                "error": "Internal Server Error",
                "message": "Lỗi hệ thống nội bộ, vui lòng thử lại sau!",
                "data": str(exc) if request.app.debug else None,
                "timestamp": datetime.now().isoformat()
            }
        )