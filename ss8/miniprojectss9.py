from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from datetime import datetime, timezone

app = FastAPI()

tickets_db = [
    {
        "id": 1,
        "movie_name": "Doctor Strange 3",
        "room_code": "IMAX-01",
        "quantity": 2,
        "status": "confirmed",
        "created_at": "2026-07-01T19:00:00Z"
    },
    {
        "id": 2,
        "movie_name": "Avatar 3",
        "room_code": "PREMIUM-02",
        "quantity": 1,
        "status": "confirmed",
        "created_at": "2026-07-01T20:15:00Z"
    }
]


class TicketCreate(BaseModel):
    movie_name: str = Field(..., min_length=1)
    room_code: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1, le=10)


def response_data(status_code, message, data, error, path):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "path": path
    }


@app.get("/tickets")
def get_tickets(request: Request):
    return response_data(
        200,
        "Lấy danh sách vé thành công!",
        tickets_db,
        None,
        request.url.path
    )


@app.post("/tickets", status_code=201)
def create_ticket(ticket: TicketCreate, request: Request):
    for item in tickets_db:
        if (
            item["movie_name"].lower() == ticket.movie_name.lower()
            and item["room_code"].lower() == ticket.room_code.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail="Lỗi: Vé xem phim tại phòng chiếu này đã được đặt!"
            )

    new_ticket = {
        "id": tickets_db[-1]["id"] + 1 if tickets_db else 1,
        "movie_name": ticket.movie_name,
        "room_code": ticket.room_code,
        "quantity": ticket.quantity,
        "status": "confirmed",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    tickets_db.append(new_ticket)

    return response_data(
        201,
        "Đặt vé thành công!",
        new_ticket,
        None,
        request.url.path
    )

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, request: Request):
    for ticket in tickets_db:
        if ticket["id"] == ticket_id:
            tickets_db.remove(ticket)

            return response_data(
                200,
                "Hủy vé thành công!",
                None,
                None,
                request.url.path
            )

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy mã vé."
    )
