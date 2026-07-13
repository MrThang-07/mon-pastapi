from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from model import Employee
from fastapi import FastAPI , HTTPException
from schemas import table_employees
def get_all_employee(db : Session):
    return db.query(Employee).all()

def get_search_employee(db : Session,department_employee :str):
    return db.query(Employee).filter(Employee.department.ilike(f"%{department_employee}%")).all()
def get_employee_id(db : Session , employee_id:int):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(
            status_code=404,
            detail= "Không tìm thấy !"
        )
    return db_employee
def post_employee(db : Session , table : table_employees):
    try:
        new_employee = Employee(
        full_name = table.full_name,
        department = table.department,
        position = table.position,
        salary = table.salary
        )
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        return new_employee
    except SQLAlchemyError :
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail= "Lỗi database không xác định"
        )
def put_employee(db : Session , employee_id:int ,table:table_employees):
    try:
        db_employee = get_employee_id(db , employee_id)
        if db_employee:
            db_employee.full_name = table.full_name
            db_employee.department = table.department
            db_employee.position = table.position
            db_employee.salary = table.salary
            db.commit()
            db.refresh(db_employee)
            return db_employee
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail= "Lỗi database không xác định"
        )
def delete_employee(db : Session , employee_id:int):
    db_employee = get_employee_id(db , employee_id)
    if db_employee:
        db.delete(db_employee)
        db.commit()
        return db_employee
    if db_employee is None:
        raise HTTPException(
            status_code=404,
            detail= "Không tìm thấy !"
        )