from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import models
import schemas

def create_parking_slot(db: Session, slot: schemas.ParkingSlotCreate):
    new_slot = models.ParkingSlot(
        slot_code=slot.slot_code,
        zone_name=slot.zone_name,
        max_weight=slot.max_weight,
        is_available=slot.is_available
    )
    
    try:
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
        return new_slot
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Mã vị trí đỗ đã tồn tại.")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Lỗi hệ thống khi lưu dữ liệu.")

def get_all_slots(db: Session):
    return db.query(models.ParkingSlot).all()

def get_slot_by_id(db: Session, slot_id: int):
    slot = db.query(models.ParkingSlot).filter(models.ParkingSlot.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    return slot