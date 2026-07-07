from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ==========================================
# 1. CẤU HÌNH DATABASE
# ==========================================
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/ecommerce_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_name = Column(String(100))
    total_price = Column(Integer)

app = FastAPI()

# ==========================================
# 2. HÀM QUẢN LÝ KẾT NỐI (TỰ ĐỘNG ĐÓNG SESSION)
# ==========================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        # LUÔN LUÔN đóng kết nối để giải phóng RAM cho MySQL
        db.close()

# ==========================================
# 3. API CONTROLLER
# ==========================================
@app.get("/orders/{order_id}")
def get_order_detail(order_id: int, db: Session = Depends(get_db)):
    # BƯỚC 1: Truy vấn dữ liệu an toàn bằng .first()
    # Nếu tìm thấy id=999, order = đối tượng OrderModel. 
    # Nếu không tìm thấy, order = None (chương trình không bị crash)
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    
    # BƯỚC 2: Kiểm tra dữ liệu rỗng và xử lý ngoại lệ có kiểm soát
    if not order:
        # Chủ động ném lỗi 404 Not Found kèm thông báo thân thiện.
        # Hệ thống không bị lộ Stack Trace (cấu trúc thư mục, code SQL) ra ngoài.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} does not exist in the system."
        )
        
    # BƯỚC 3: Trả về dữ liệu nếu tìm thấy
    return {"id": order.id, "customer": order.customer_name}