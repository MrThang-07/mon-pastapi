from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Khởi tạo động cơ kết nối
engine = create_engine(settings.DATABASE_URL)

# Tạo phiên làm việc
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Lớp cơ sở để các Model kế thừa
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()