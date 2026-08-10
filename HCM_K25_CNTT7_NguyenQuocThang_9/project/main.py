from fastapi import FastAPI , Depends 
from pydantic import BaseModel 
from database import Base , engine , get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.get("/")
def helloserver(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return{
        "massage": "KET NOI THANH CONG"
    }