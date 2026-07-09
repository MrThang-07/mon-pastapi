from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Chuỗi kết nối MySQL (Bạn có thể đổi tên db thành pet_boarding_db nếu muốn)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/pet_boarding_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()