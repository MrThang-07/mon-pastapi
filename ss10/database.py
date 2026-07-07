from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Định nghĩa chuỗi kết nối (Connection string)
# Lưu ý: Thay thế user, password, host, port và tên database của bạn vào đây
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/task_manager"

# 2. Khởi tạo đối tượng Engine quản lý Connection Pool
engine = create_engine(DATABASE_URL)

# 3. Khởi tạo Factory SessionLocal dùng để sinh ra Session
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# 4. Generator function quản lý vòng đời của Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()