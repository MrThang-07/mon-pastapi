from fastapi import FastAPI , Depends , HTTPException
from database import Base , engine , get_db 
import crud
import schemas
from sqlalchemy.orm import Session

Base.metadata.create_all(bind = engine)
app = FastAPI()

@app.get("/")
def check_server():
    return "Hello!"
@app.get("/teams")
def get_all_team(db : Session = Depends(get_db)):
    db_team = crud.get_all_team(db)
    return {
        "message" : "Lay danh sach toan bo doi tuyen ",
        "data": db_team
    }
@app.get("/teams/search")
def search_team(keyword : str , db : Session = Depends(get_db)):
    db_team = crud.search_team(db,keyword)
    return {
        "message" : "Da tim kiem đội tuyển  ",
        "data": db_team
    }   
@app.get("/teams/sort")
def sort_team(choice : str = "asc" ,  db : Session = Depends(get_db)):
    db_team = crud.sort_team(db ,choice)
    return {
        "message" : "Sắp xếp theo group_name (hỗ trợ asc hoặc desc).",
        "data": db_team
    }  

@app.get("/teams/{team_id}")
def get_team_id(team_id : int , db : Session = Depends(get_db)):
    db_team = crud.get_team_id(db , team_id)
    return {
        "message" : "Lấy chi tiết đội tuyển theo ID .",
        "data": db_team
    } 
@app.post("/teams")
def post_team(table_team : schemas.table, db : Session = Depends(get_db)):
    db_team = crud.post_teams(db , table_team)
    return {
        "message" : "Thêm mới một đội tuyển thanh cong",
        "data": db_team
    }  
@app.put("/teams/{team_id}")
def update_team(team_id : int ,table_team : schemas.table, db : Session = Depends(get_db)):
    db_team = crud.update_team(db ,table_team,team_id )
    return {
        "message" : "Cập nhật thông tin đội tuyển theo ID thanh cong",
        "data": db_team
    }   
@app.delete("/teams/{team_id}")
def delete_team(team_id : int , db : Session = Depends(get_db)):
    db_team = crud.delete_team(db , team_id)
    return {
        "message" : "Da Xóa đội tuyển theo ID. ",
        "data": db_team
    }   




