from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional, Any

# Quy chuẩn Status bằng Enum
class StatusEnum(str, Enum):
    AVAILABLE = "AVAILABLE"
    OUT_OF_STOCK = "OUT_OF_STOCK"

# Khuôn hứng dữ liệu tạo mới
class MenuItemBase(BaseModel):
    dish_code: str = Field(..., max_length=50)
    dish_name: str = Field(..., min_length=1, max_length=100)
    calorie_count: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    status: StatusEnum = StatusEnum.AVAILABLE

# Khuôn hứng dữ liệu cập nhật (Cho phép bỏ trống trường không cần sửa)
class MenuItemUpdate(BaseModel):
    dish_code: Optional[str] = Field(None, max_length=50)
    dish_name: Optional[str] = Field(None, min_length=1, max_length=100)
    calorie_count: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[StatusEnum] = None

# Khuôn xuất dữ liệu (Có thêm ID, bật ConfigDict để đọc Object từ Database)
class MenuItemResponse(MenuItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Khung Response chuẩn 6 trường theo yêu cầu đề bài
class StandardResponse(BaseModel):
    statusCode: int
    message: str
    error: Optional[str] = None
    data: Optional[Any] = None
    path: str
    timestamp: str