from fastapi import FastAPI ,Depends,HTTPException
from database import Base , engine , get_db
from sqlalchemy.orm import Session
import crud
import schemas
Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get("/")
def check_team():
    return "Hello !"
@app.get("/teams/search")
def search_team(keyword :str,db : Session = Depends(get_db)):
    return crud.search_team(db , keyword)
@app.get("/teams/sort")
def sort_team(choice: str = "asc" ,db : Session = Depends(get_db)):
    return crud.sort_team(db,choice)

@app.get("/teams")
def get_allteam(db : Session = Depends(get_db)):
    return crud.get_allteam(db)
@app.get("/teams/{team_id}")
def get_team_id(get_id :int,db : Session = Depends(get_db)):
    db_team = crud.get_team_id(db , get_id)
    if not db_team:
        raise HTTPException(status_code=404,detail="khong tim thay")
    return db_team
@app.post("/teams")
def post_team_id(table :schemas.table_team ,db : Session = Depends(get_db)):
    return crud.post_team(db , table)

@app.put("/teams/{team_id}")
def update_team(get_id :int, table :schemas.table_team ,db : Session = Depends(get_db)):
    db_team = crud.update_team(db ,table, get_id )
    if not db_team:
        raise HTTPException(status_code=404,detail="khong tim thay")
    return db_team
@app.delete("/teams/{team_id}")
def delete_team(get_id :int,db : Session = Depends(get_db)):
    db_team = crud.delete_team(db,get_id)
    if not db_team:
        raise HTTPException(status_code=404,detail="khong tim thay")
    return "Da xoa thanh cong"

    





