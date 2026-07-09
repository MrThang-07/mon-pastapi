from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone

# Import đích danh
from database import engine, get_db
from models import Base
from schemas import MenuItemBase, MenuItemUpdate, MenuItemResponse
from service import create_item, get_all_items, get_item_by_id, update_item, delete_item

# Lệnh tự động tạo bảng MySQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hệ thống Quản lý Suất ăn Công nghiệp API")

def get_current_timestamp():
    """Lấy thời gian chuẩn ISO 8601 UTC"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def create_standard_response(status_code: int, message: str, path: str, data=None, error=None):
    """Gói dữ liệu thành chuẩn 6 trường"""
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": get_current_timestamp()
    }

# Bắt lỗi toàn cục để không bị vỡ định dạng 6 trường
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    error_type = "Not Found" if exc.status_code == 404 else "Bad Request" if exc.status_code == 400 else "Error"
    response_content = create_standard_response(
        status_code=exc.status_code, message=exc.detail, path=request.url.path, error=error_type
    )
    return JSONResponse(status_code=exc.status_code, content=response_content)


@app.post("/menu-items")
def create_menu_item(item: MenuItemBase, request: Request, db: Session = Depends(get_db)):
    db_item = create_item(db, item)
    item_data = MenuItemResponse.model_validate(db_item).model_dump()
    return create_standard_response(201, "Thêm món ăn mới thành công", request.url.path, data=item_data)

@app.get("/menu-items")
def get_all_menu_items(request: Request, db: Session = Depends(get_db)):
    db_items = get_all_items(db)
    items_data = [MenuItemResponse.model_validate(i).model_dump() for i in db_items]
    return create_standard_response(200, "Lấy danh sách món ăn thành công", request.url.path, data=items_data)

@app.get("/menu-items/{item_id}")
def get_menu_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    db_item = get_item_by_id(db, item_id)
    item_data = MenuItemResponse.model_validate(db_item).model_dump()
    return create_standard_response(200, "Lấy thông tin món ăn thành công", request.url.path, data=item_data)

@app.put("/menu-items/{item_id}")
def update_menu_item(item_id: int, item_in: MenuItemUpdate, request: Request, db: Session = Depends(get_db)):
    db_item = update_item(db, item_id, item_in)
    updated_data = MenuItemResponse.model_validate(db_item).model_dump()
    return create_standard_response(200, "Cập nhật món ăn thành công", request.url.path, data=updated_data)

@app.delete("/menu-items/{item_id}")
def delete_menu_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    delete_item(db, item_id)
    return create_standard_response(200, "Xóa món ăn thành công", request.url.path)