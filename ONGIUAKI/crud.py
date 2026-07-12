from models import Team
from sqlalchemy.orm import Session
from schemas import table_post
def getall_lists(db : Session):
    return db.query(Team).all()

def get_id(db : Session , team_id : int):
    return db.query(Team).filter(Team.id == team_id).first()

def post_team(db : Session , table : table_post):
    new_team = Team(
        country_name = table.country_name,
        coach_name = table.coach_name,
        group_name = table.group_name
    )
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

def update_team(db : Session , get_id : int , table : table_post):
    db_team = get_id(db , get_id)
    if db_team:
        db_team.country_name = table.country_name,
        db_team.coach_name = table.coach_name,
        db_team.group_name = table.group_name
        db.commit()
        db.refresh()
    return db_team

def delete_team(db : Session , get_id : int ):
    db_team = get_id(db , get_id)
    if db_team:
        db.delete(db_team)
        db.commit()
    return db_team

def search_team(db : Session ,keyword : str):
    return db.query(Team).filter(Team.country_name.ilike(f"%{keyword}%")).all()

def sort_team(db :Session , choice : str):
    if choice == "desc":
        return db.query(Team).order_by(Team.group_name.desc()).all()
    return db.query(Team).order_by(Team.group_name.asc()).all()