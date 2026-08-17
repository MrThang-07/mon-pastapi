from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import user as user_router

# Khởi tạo bảng trong database nếu chưa có
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Manager Devconnect",
    version="1.0.0"
)

# Đăng ký router
app.include_router(user_router.router)

@app.get("/")
def get_root():
    return {"message": "Server đang được kết nối!"}