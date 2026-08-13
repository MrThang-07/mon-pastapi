from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

from database import engine, Base
from app.routers import student_router

# Tạo tất cả các bảng (1-1, 1-N, N-N) tự động vào MySQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Quản Lý Sinh Viên")

app.include_router(student_router.router)

# Hàm định dạng lỗi dùng chung cho Exception
def format_error_response(request: Request, status_code: int, message: str, error_detail: any):
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "message": message,
            "data": {},
            "error": error_detail,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": request.url.path
        }
    )

# 1. Bắt lỗi Validation (Pydantic - 422 Unprocessable Entity)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return format_error_response(request, 422, "Dữ liệu không hợp lệ", exc.errors())

# 2. Bắt lỗi Nghiệp vụ (HTTPException - 400, 404)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return format_error_response(request, exc.status_code, exc.detail, exc.detail)