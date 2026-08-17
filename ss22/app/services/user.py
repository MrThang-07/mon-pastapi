from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import HTTPException
from app.cores.security import hash_password

def create_user(db: Session, user: UserCreate):
    exist_user = db.query(User).filter(User.username == user.username).first()
    if exist_user:
        raise HTTPException(status_code=400, detail="User da ton tai")
    
    hashed_pwd = hash_password(user.password)
    
    new_user = User(
        username=user.username,
        hashed_password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user