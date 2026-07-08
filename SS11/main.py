from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from datetime import datetime, timezone

import models
import schemas
import services
from database import engine, get_db

# Khởi tạo bảng nếu chưa có
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- FORMAT RESPONSE & EXCEPTION ---
def format_response(status_code: int, message: str, error: str | None, data: any, path: str):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=format_response(exc.status_code, exc.detail, "Error", None, request.url.path)
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=format_response(422, "Dữ liệu đầu vào không hợp lệ", str(exc.errors()), None, request.url.path)
    )

# --- API ENDPOINTS ---
@app.post("/parking-slots")
def create_slot(slot: schemas.ParkingSlotCreate, request: Request, db: Session = Depends(get_db)):
    result = services.create_parking_slot(db, slot)
    
    data = {
        "id": result.id, "slot_code": result.slot_code,
        "zone_name": result.zone_name, "max_weight": result.max_weight,
        "is_available": result.is_available
    }
    
    return format_response(201, "Thêm vị trí đỗ xe thành công", None, data, request.url.path)

@app.get("/parking-slots")
def get_slots(request: Request, db: Session = Depends(get_db)):
    slots = services.get_all_slots(db)
    data = [{"id": s.id, "slot_code": s.slot_code, "zone_name": s.zone_name, "max_weight": s.max_weight, "is_available": s.is_available} for s in slots]
    return format_response(200, "Thành công", None, data, request.url.path)

@app.get("/parking-slots/{slot_id}")
def get_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    result = services.get_slot_by_id(db, slot_id)
    data = {"id": result.id, "slot_code": result.slot_code, "zone_name": result.zone_name, "max_weight": result.max_weight, "is_available": result.is_available}
    return format_response(200, "Thành công", None, data, request.url.path)