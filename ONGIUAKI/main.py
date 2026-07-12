from database import Base, get_db, engine
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session 

import crud 

from schemas import table_post

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def getcheck():
    return "Hello !"

@app.get("/teams/search")
def search_team(keyword: str, db: Session = Depends(get_db)):
    return crud.search_team(db, keyword) 

@app.get("/teams/sort")
def sort_team(order: str, db: Session = Depends(get_db)):
    return crud.sort_team(db, order)

@app.get("/teams")
def getall_list(db: Session = Depends(get_db)):
    return crud.getall_lists(db)

@app.get("/teams/{team_id}")
def get_list_id(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_id(db, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Khong tim thay !")
    return db_team

@app.post("/teams")
def post_team(team: table_post, db: Session = Depends(get_db)):
    return crud.post_team(db, team)

@app.put("/teams/{team_id}")
def update_team(team_id: int, table: table_post, db: Session = Depends(get_db)):
    db_team = crud.update_team(db, team_id, table)
    if not db_team:
        raise HTTPException(status_code=404, detail="Khong tim thay !")
    return db_team

@app.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.delete_team(db, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Khong tim thay !")
    return {"message": "da xoa thanh cong"}