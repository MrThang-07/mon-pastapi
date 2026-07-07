from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# 1. CẤU HÌNH DATABASE
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/ecommerce_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. TẦNG LƯU TRỮ (Entity / Database Model)
class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

# 3. TẦNG GIAO TIẾP (DTO / Pydantic Schema)
class ProductCreate(BaseModel):
    sku: str
    name: str
    price: float

app = FastAPI()

# 4. HÀM QUẢN LÝ KẾT NỐI (Tự động đóng/mở Session)
def get_db():
    db = SessionLocal()
    try:
        yield db  # Trả DB cho API sử dụng
    finally:
        db.close() # Tự động đóng kết nối khi API chạy xong

# 5. API CONTROLLER
@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        # Map dữ liệu từ Schema (product) sang Entity (ProductModel)
        new_product = ProductModel(
            sku=product.sku,
            name=product.name,
            price=product.price
        )
        
        db.add(new_product)
        db.commit()          # Lưu vĩnh viễn xuống ổ cứng
        db.refresh(new_product) # Lấy id tự tăng từ Database lên
        
        return {
            "message": "Product created successfully", 
            "data": {
                "id": new_product.id,
                "sku": new_product.sku, 
                "name": new_product.name
            }
        }
        
    except Exception as e:
        db.rollback() # Hoàn tác nếu có lỗi (vd: trùng mã SKU)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Database error: {str(e)}"
        )