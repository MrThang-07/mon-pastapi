from sqlalchemy.orm import Session
from model import Team
from schemas import table
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
def get_all_team(db : Session):
    return db.query(Team).all()

def get_team_id(db : Session , team_id : int):
    result = db.query(Team).filter(Team.id == team_id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Id khong ton tai")
    return result
def post_teams(db : Session , table_team : table):
    try:
        new_team = Team(
            country_name = table_team.country_name,
            coach_name = table_team.coach_name,
            group_name = table_team.group_name
        )
        db.add(new_team)
        db.commit()
        db.refresh(new_team)
        return new_team
    except SQLAlchemyError :
        db.rollback()
        raise HTTPException(status_code=500 , detail="Loi database khong xac dinh ")

def update_team(db : Session , table_team : table , team_id:int):
    try:
        db_team = get_team_id(db , team_id)
        if db_team :
            db_team.country_name = table_team.country_name
            db_team.coach_name = table_team.coach_name
            db_team.group_name = table_team.group_name
        db.commit()
        db.refresh(db_team)
        return db_team
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException (status_code=500 , detail="Loi database khong xac dinh")
def delete_team(db : Session , team_id : int):
    db_team = get_team_id(db , team_id)
    if db_team :
        db.delete(db_team)
        db.commit()
        return db_team
    
def search_team(db : Session , keyword:str):
    db_team = db.query(Team).filter(Team.country_name.ilike(f"%{keyword}%")).all()
    return db_team 
def sort_team(db : Session , choice:str = "asc"):
    if choice == "desc":
        return db.query(Team).order_by(Team.group_name.desc()).all()
    return db.query(Team).order_by(Team.group_name.asc()).all()