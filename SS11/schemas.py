from pydantic import BaseModel, Field

class ParkingSlotCreate(BaseModel):
    slot_code: str = Field(..., max_length=50)
    zone_name: str = Field(..., min_length=3, max_length=255)
    max_weight: int = Field(..., gt=0)
    is_available: bool = Field(default=True)