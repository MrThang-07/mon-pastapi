from database import Base , engine
from fastapi import FastAPI
from app.models.student_model import table_database
from app.routers.student_router import student_router


app = FastAPI()
Base.metadata.create_all(bind = engine)
app.include_router(student_router)
@app.get("/")
def check():
    return "Hello server"

