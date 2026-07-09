from sqlalchemy.orm import Session
from fastapi import HTTPException

# Import đích danh các class cần thiết
from models import MenuItem
from schemas import MenuItemBase, MenuItemUpdate

def get_all_items(db: Session):
    return db.query(MenuItem).all()

def get_item_by_id(db: Session, item_id: int):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

def create_item(db: Session, item: MenuItemBase):
    # Kiểm tra trùng lặp mã món ăn
    existing_item = db.query(MenuItem).filter(MenuItem.dish_code == item.dish_code).first()
    if existing_item:
        raise HTTPException(status_code=400, detail="Mã món ăn đã tồn tại")
    
    try:
        # Bung dữ liệu từ dictionary vào Model
        new_item = MenuItem(**item.model_dump())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Lỗi hệ thống khi thêm dữ liệu")

def update_item(db: Session, item_id: int, item_in: MenuItemUpdate):
    db_item = get_item_by_id(db, item_id)
        
    # Kiểm tra trùng lặp nếu người dùng đổi mã dish_code
    if item_in.dish_code and item_in.dish_code != db_item.dish_code:
        duplicate = db.query(MenuItem).filter(MenuItem.dish_code == item_in.dish_code).first()
        if duplicate:
            raise HTTPException(status_code=400, detail="Mã món ăn cập nhật bị trùng lặp")

    try:
        # Lọc ra những trường được gửi lên
        update_data = item_in.model_dump(exclude_unset=True)
        
        # Ghi đè dữ liệu mới
        for field, value in update_data.items():
            setattr(db_item, field, value)
            
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Lỗi hệ thống khi cập nhật dữ liệu")

def delete_item(db: Session, item_id: int):
    db_item = get_item_by_id(db, item_id)
    try:
        db.delete(db_item)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Lỗi hệ thống khi xóa dữ liệu")