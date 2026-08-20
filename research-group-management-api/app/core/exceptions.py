from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

def setup_exception_handlers(app: FastAPI):
    # 1. Bắt các lỗi HTTP  (400, 401, 403, 404)
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "code": exc.status_code,
                "message": exc.detail
            }
        )

    # 2. Bắt lỗi 422 - Validate dữ liệu (Khi Pydantic Schema chặn lại do sai format)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "code": 422,
                "message": "Dữ liệu đầu vào không hợp lệ",
                "details": exc.errors()  # Chi tiết trường nào bị sai
            }
        )

    # 3. Bắt lỗi hệ thống 500 (Tránh việc sập server hiển thị code thô ra ngoài)
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "code": 500,
                "message": "Lỗi hệ thống nội bộ, vui lòng thử lại sau!"
            }
        )