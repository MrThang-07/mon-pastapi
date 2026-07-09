from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import BoardingSlot
from schemas import BoardingSlotBase, BoardingSlotUpdate

def get_all_slots(db: Session):
    return db.query(BoardingSlot).all()

def get_slot_by_id(db: Session, slot_id: int):
    slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    return slot

def create_slot(db: Session, slot_in: BoardingSlotBase):
    # Ràng buộc không trùng lặp slot_number
    existing_slot = db.query(BoardingSlot).filter(BoardingSlot.slot_number == slot_in.slot_number).first()
    if existing_slot:
        raise HTTPException(status_code=400, detail="Slot number already exists")
    
    try:
        new_slot = BoardingSlot(**slot_in.model_dump())
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
        return new_slot
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Lỗi hệ thống khi thêm khoang lưu trú")

def update_slot(db: Session, slot_id: int, slot_in: BoardingSlotUpdate):
    db_slot = get_slot_by_id(db, slot_id)
        
    # Kiểm tra nếu update slot_number thì có trùng với khoang khác không
    if slot_in.slot_number and slot_in.slot_number != db_slot.slot_number:
        duplicate = db.query(BoardingSlot).filter(BoardingSlot.slot_number == slot_in.slot_number).first()
        if duplicate:
            raise HTTPException(status_code=400, detail="Slot number already exists")

    try:
        update_data = slot_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_slot, field, value)
            
        db.commit()
        db.refresh(db_slot)
        return db_slot
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Lỗi hệ thống khi cập nhật thông tin")

def delete_slot(db: Session, slot_id: int):
    db_slot = get_slot_by_id(db, slot_id)
    try:
        db.delete(db_slot)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Lỗi hệ thống khi xóa khoang lưu trú")