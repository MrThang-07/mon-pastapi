from sqlalchemy.orm import Session , joinedload  
from sqlalchemy.exc import SQLAlchemyError
from app.models.student_model import StudentModel
from app.schemas.student_schema import StudentCreateDTO
from fastapi import HTTPException 
def get_all_student(db: Session, offset : int , limit : int):
    return db.query(StudentModel).options(joinedload(StudentModel.department)).offset(offset).limit(limit).all()

def get_student(db : Session , student_id : int):
    result =  db.query(StudentModel).options(joinedload(StudentModel.department)).filter(StudentModel.id == student_id).first()
    if result is None:
        raise HTTPException(status_code=404,detail="khong tim thay sinh vien")
    

def create_student(db: Session,student :StudentCreateDTO  ):
    try:
        new_student = StudentModel(
            name = student.name,
            age = student.age,
            department_id = student.department_id
        )
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
    except SQLAlchemyError:
        raise HTTPException(status_code=500,detail="khong xac dinh")