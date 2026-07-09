from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from database import engine, get_db
from models import Base
from schemas import BoardingSlotBase, BoardingSlotUpdate, BoardingSlotResponse
from service import create_slot, get_all_slots, get_slot_by_id, update_slot, delete_slot

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hệ thống Đặt chỗ Dịch vụ Chăm sóc Thú cưng API")

def get_current_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def create_standard_response(status_code: int, message: str, path: str, data=None, error=None):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": get_current_timestamp()
    }

# Bắt lỗi toàn cục để đồng nhất chuẩn 6 trường
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    error_type = "Not Found" if exc.status_code == 404 else "Bad Request" if exc.status_code == 400 else "Error"
    response_content = create_standard_response(
        status_code=exc.status_code, 
        message=exc.detail, 
        path=request.url.path, 
        error=error_type
    )
    return JSONResponse(status_code=exc.status_code, content=response_content)


@app.post("/boarding-slots")
def api_create_slot(slot: BoardingSlotBase, request: Request, db: Session = Depends(get_db)):
    db_slot = create_slot(db, slot)
    slot_data = BoardingSlotResponse.model_validate(db_slot).model_dump()
    return create_standard_response(201, "Thêm khoang lưu trú thành công", request.url.path, data=slot_data)

@app.get("/boarding-slots")
def api_get_all_slots(request: Request, db: Session = Depends(get_db)):
    db_slots = get_all_slots(db)
    slots_data = [BoardingSlotResponse.model_validate(i).model_dump() for i in db_slots]
    return create_standard_response(200, "Lấy danh sách thành công", request.url.path, data=slots_data)

@app.get("/boarding-slots/{slot_id}")
def api_get_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    db_slot = get_slot_by_id(db, slot_id)
    slot_data = BoardingSlotResponse.model_validate(db_slot).model_dump()
    return create_standard_response(200, "Lấy chi tiết khoang lưu trú thành công", request.url.path, data=slot_data)

@app.put("/boarding-slots/{slot_id}")
def api_update_slot(slot_id: int, slot_in: BoardingSlotUpdate, request: Request, db: Session = Depends(get_db)):
    db_slot = update_slot(db, slot_id, slot_in)
    updated_data = BoardingSlotResponse.model_validate(db_slot).model_dump()
    return create_standard_response(200, "Cập nhật khoang lưu trú thành công", request.url.path, data=updated_data)

@app.delete("/boarding-slots/{slot_id}")
def api_delete_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    delete_slot(db, slot_id)
    return create_standard_response(200, "Xóa khoang lưu trú thành công", request.url.path)