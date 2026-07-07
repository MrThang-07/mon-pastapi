from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cau hinh ket noi
# Connection string
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/school_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine
)

# Khai bao base class de dinh nghia model
Base = declarative_base() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()