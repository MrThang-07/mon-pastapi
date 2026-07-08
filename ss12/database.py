from sqlalchemy import create_engine   
from sqlalchemy.orm import sessionmaker , declarative_base

DATABASE_URL ="mysql+pymysql://root:123456@localhost:3306/uses_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,bind=engine,autoflush=False)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

Base = declarative_base()
