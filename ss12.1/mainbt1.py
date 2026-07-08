from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ==========================================
# CẤU HÌNH DATABASE
# ==========================================
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/ecommerce_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()

# ==========================================
# MODEL & SCHEMA
# ==========================================
class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

class ProductUpdate(BaseModel):
    name: str
    price: float

app = FastAPI()

# ==========================================
# 1. DEPENDENCY QUẢN LÝ SESSION
# ==========================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # Đảm bảo đóng kết nối để tránh treo database (Giải quyết Bẫy 2)

# ==========================================
# 2. API CẬP NHẬT SẢN PHẨM
# ==========================================
@app.put("/products/{product_id}")
def update_product(
    product_id: int, 
    product_update: ProductUpdate, 
    db: Session = Depends(get_db) # Tiêm dependency
):
    # Tìm sản phẩm trong DB
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()

    # Báo lỗi 404 đúng chuẩn nếu không tìm thấy
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # Cập nhật dữ liệu trên object Python
    product.name = product_update.name
    product.price = product_update.price

    # Lưu thay đổi vào MySQL (Giải quyết Bẫy 1)
    db.commit()
    
    # Làm mới object để lấy dữ liệu mới nhất từ CSDL
    db.refresh(product)

    return {
        "message": "Product updated successfully",
        "data": {
            "id": product.id,
            "name": product.name,
            "price": product.price
        }
    }