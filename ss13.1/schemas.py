from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional, Any

# Quy chuẩn dữ liệu bằng Enum
class RoomSizeEnum(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class StatusEnum(str, Enum):
    VACANT = "VACANT"
    OCCUPIED = "OCCUPIED"

class BoardingSlotBase(BaseModel):
    slot_number: str = Field(..., max_length=50)
    room_size: RoomSizeEnum
    price_per_day: float = Field(..., gt=0, description="Giá mỗi ngày phải lớn hơn 0")
    status: StatusEnum = StatusEnum.VACANT

class BoardingSlotUpdate(BaseModel):
    slot_number: Optional[str] = Field(None, max_length=50)
    room_size: Optional[RoomSizeEnum] = None
    price_per_day: Optional[float] = Field(None, gt=0)
    status: Optional[StatusEnum] = None

class BoardingSlotResponse(BoardingSlotBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Khung Response chuẩn 6 trường
class StandardResponse(BaseModel):
    statusCode: int
    message: str
    error: Optional[str] = None
    data: Optional[Any] = None
    path: str
    timestamp: str