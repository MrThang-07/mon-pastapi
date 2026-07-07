from fastapi import FastAPI, Request, HTTPException, status
from pydantic import BaseModel, Field
from typing import Any, Optional
from datetime import datetime, timezone, UTC
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI(
    title = "Cinema ticket booking API",
    description = "API hệ thống Đặt vé xem phim online"
)

class TicketRequestDTO(BaseModel):
    movie_name: str = Field(..., min_length=1)
    room_code: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1, le=10)

class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
    timestamp: str
    path: str

def success_response(statusCode: int, message: str, data: Any, error: Any, request: Request):
    return APIResponse(
        statusCode = statusCode,
        message = message,
        data = data,
        error = error,
        timestamp = datetime.now(timezone.utc).isoformat(),
        path = request.url.path
    )

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code = 404,
        content = APIResponse(
            statusCode =  exc.status_code,
            message = exc.detail,
            timestamp = datetime.now(timezone.utc).isoformat(),
            path = request.url.path
        ).model_dump()
    )

@app.exception_handler(RequestValidationError)
def http_ValidationError_exception(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=APIResponse(
            statusCode=422,
            message="Dữ liệu không hợp lệ",
            error=exc.errors(),
            timestamp=datetime.now(timezone.utc).isoformat(),
            path = request.url.path
        ).model_dump()
    )

tickets_db = [
    {"id": 1, "movie_name": "Doctor Strange 3", "room_code": "IMAX-01", "quantity": 2, "status": "confirmed", "created_at": "2026-07-01T19:00:00Z"},
    {"id": 2, "movie_name": "Avatar 3", "room_code": "PREMIUM-02", "quantity": 1, "status": "confirmed", "created_at": "2026-07-01T20:15:00Z"}
]

@app.get("/tickets", tags = ["Tickets"], status_code=status.HTTP_200_OK)
def get_tickets(request: Request):
    if not tickets_db:
        raise HTTPException(status_code=404, detail="Not Found")
    return success_response(200, "Lấy dữ liệu thành công", tickets_db, None, request)

@app.post("/tickets", tags=["Tickets"], status_code=status.HTTP_201_CREATED)
def create_tickets(ticket: TicketRequestDTO, request: Request):
    ticket_id = max(t["id"] for t in tickets_db) + 1
    new_ticket = {
        "id": ticket_id,
        "movie_name": ticket.movie_name,
        "room_code": ticket.room_code,
        "quantity": ticket.quantity,
        "status": "confirmed",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    tickets_db.append(new_ticket)
    return success_response(201, "Thêm thành công", new_ticket, None, request)

@app.delete("/tickets/{ticket_id}")
def remove_tickets(ticket_id: int, request: Request):
    find_ticket = next((t for t in tickets_db if t["id"] == ticket_id), None)
    if not find_ticket:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
    tickets_db.remove(find_ticket)
    return success_response(200, "Xóa thành công", find_ticket, None, request)