from sqlalchemy.orm import sessionmaker , declarative_base
from sqlalchemy import create_engine
DATABASE_URL = "mysql+pymysql://root:123456@localhost/worldcup_db"

engine = create_engine(DATABASE_URL)
SessionLocal =sessionmaker(
    autocommit = False,
    bind= engine,
    autoflush= False
)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
