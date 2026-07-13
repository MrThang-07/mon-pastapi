from fastapi import FastAPI , Depends ,status
from database import engine , Base , get_db
import employee_services
from sqlalchemy.orm import Session
from schemas import table_employees
Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get("/")
def check_server():
    return {"message" : "API đang chạy",
            "data": "null"}
@app.get("/employees", status_code=status.HTTP_200_OK)
def get_all_employee(db : Session = Depends(get_db)):
    db_employee = employee_services.get_all_employee(db)
    return {
        "statusCode":200,
        "error": "null",
        "message": "Đã lấy danh sách nhân viên ",
        "data":db_employee
    }
@app.get("/employees/search",status_code=status.HTTP_200_OK)
def get_search_employee(keyword : str ,db : Session = Depends(get_db)):
    db_employee = employee_services.get_search_employee(db ,keyword)
    return {
        "statusCode":200,
        "error": "null",
        "message":"Đã tìm kiếm theo phòng ban",
        "data": db_employee
    }
@app.get("/employees/{employee_id}",status_code=status.HTTP_200_OK)
def get_employee_id(employee_id:int ,db : Session = Depends(get_db) ):
    db_employee = employee_services.get_employee_id(db , employee_id)
    return {
        "statusCode":200,
        "error": "null",
        "message": "Đã lấy chi tiết nhân viên",
        "data": db_employee
    }
@app.post("/employees",status_code=status.HTTP_201_CREATED)
def post_employee(table :table_employees ,db : Session = Depends(get_db)):
    db_employee = employee_services.post_employee(db , table)
    return {
        "statusCode":201,
        "error": "null",
        "massage": "Đã thêm mới",
        "data": db_employee
    }
@app.put("/employees/{employee_id}")
def put_employees(employee_id:int ,table :table_employees ,db : Session = Depends(get_db)):
    db_employee = employee_services.put_employee(db ,employee_id,table)
    return {
        "statusCode":200,
        "error": "null",
        "message": "Đã cập nhật ",
        "data" : db_employee
    }
@app.delete("/employees/{employee_id}")
def delete_employees(employee_id:int ,db : Session = Depends(get_db)):
    db_employee = employee_services.delete_employee(db , employee_id)
    return {
        "statusCode":200,
        "error": "null",
        "massage": "Đã xóa !",
        "data": db_employee
    }

