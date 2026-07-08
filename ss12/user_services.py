from sqlalchemy.orm import Session
from schemas import UsersRequestDTO
from models import UsersModel
from fastapi import HTTPException
# Ham them du lieu 
def create_user(db: Session , user :UsersRequestDTO):
    try: 
        new_user = UsersModel(
            name = user.name,
            email = user.email
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Loi trong qua trinh them ")

#lay ra user
def get_user(db : Session , user_id: int):
    return db.query(UsersModel).filter(UsersModel.id == user_id).first()
    