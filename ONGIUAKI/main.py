from fastapi import FastAPI, Depends, HTTPException
from database import Base, engine, get_db
from sqlalchemy.orm import Session
import crud
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def check_team():
    return {"message": "Server is running normally!"}

@app.get("/teams/search")
def search_team(keyword: str, db: Session = Depends(get_db)):
    teams = crud.search_team(db, keyword)
    return {
        "message": "Tìm kiếm thành công",
        "data": teams
    }

@app.get("/teams/sort")
def sort_team(choice: str = "asc", db: Session = Depends(get_db)):
    teams = crud.sort_team(db, choice)
    return {
        "message": "Sắp xếp thành công",
        "data": teams
    }

@app.get("/teams")
def get_allteam(db: Session = Depends(get_db)):
    teams = crud.get_allteam(db)
    return {
        "message": "Lấy danh sách thành công",
        "data": teams
    }

@app.get("/teams/{team_id}")
def get_team_id(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team_id(db, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Không tìm thấy đội bóng")
    return {
        "message": "Lấy thông tin chi tiết thành công",
        "data": db_team
    }

@app.post("/teams")
def post_team_id(table: schemas.table_team, db: Session = Depends(get_db)):
    new_team = crud.post_team(db, table)
    return {
        "message": "Thêm mới thành công",
        "data": new_team
    }

@app.put("/teams/{team_id}")
def update_team(team_id: int, table: schemas.table_team, db: Session = Depends(get_db)):
    db_team = crud.update_team(db, table, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Không tìm thấy đội bóng để cập nhật")
    return {
        "message": "Cập nhật thành công",
        "data": db_team
    }

@app.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.delete_team(db, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Không tìm thấy đội bóng để xóa")
    return {
        "message": "Đã xóa thành công",
        "data": db_team
    }