from fastapi import FastAPI, Depends,HTTPException
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import get_db , Base ,engine
from database import *
from schemas import UsersRequestDTO
app = FastAPI()
from user_services import create_user ,get_user


Base.metadata.create_all(bind = engine)
@app.get("/test")
def test_connections(db: Session = Depends(get_db)):
    try:
        db.execute(text('SELECT 1'))
        return {
            "message": "Ket noi thanh cong"
        }
    except Exception as e:
        raise HTTPException(status_code = 400, detail = "Ket noi that bai")
# api them user
@app.post("/user")
def add_users(user: UsersRequestDTO,db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400,detail="Them khong thanh cong")
    return {
        "status_code":201,
        "massage": "Them thanh cong",
        "data":db_user
    }
# api lay user
@app.get("/users/{users_id}")
def get_users(user_id = int ,db: Session = Depends(get_db)):
    db_user = get_user(db ,user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail="Id Not Found")
    return{
        "status_code": 200,
        
        "massage": "Lay thong tin thanh cong",
        "data": db_user
    }
    

