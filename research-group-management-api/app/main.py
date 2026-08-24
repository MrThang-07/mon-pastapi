from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import cấu hình và database
from app.core.config import settings
from app.db.database import engine, Base
from app.models.user import User
from app.models.research_project import ResearchProject, ResearchMember
from app.models.research_task import ResearchTask
from app.routers import auth, users
from app.core.exceptions import setup_exception_handlers
from app.routers import research_projects

Base.metadata.create_all(bind=engine)

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="Hệ thống API Quản lý Nhóm Nghiên cứu Khoa học",
    version="1.0.0"
)
setup_exception_handlers(app)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(research_projects.router)
# Cấu hình CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức GET, POST, PUT, DELETE...
    allow_headers=["*"],  # Cho phép tất cả các loại Header
)


# API test server
@app.get("/health-check")
def health_check():
    return {
        "status": "success", 
        "message": "Hệ thống đang hoạt động bình thường!"
    }