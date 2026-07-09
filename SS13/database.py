from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Chuỗi kết nối MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/catering_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Cung cấp session cho mỗi API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()