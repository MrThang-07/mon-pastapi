from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

# Import generator function từ file database.py cùng thư mục
from database import get_db

app = FastAPI(title="Demo Database Connection API")

@app.get("/test-connection")
def test_connection(db: Session = Depends(get_db)):
    try:
        # Thực hiện câu lệnh truy vấn đơn giản để kiểm tra kết nối
        db.execute(text('SELECT 1'))
        
        return {
            "status": "success",
            "message": "Kết nối thành công!"
        }
    except Exception as e:
        # Bắt lỗi và trả về HTTP 500 nếu kết nối thất bại
        raise HTTPException(
            status_code=500,
            detail=f"Kết nối thất bại. Lỗi: {str(e)}"
        )
    
@app.get("/test-data")
def test_data(db: Session = Depends(get_db)):
    try:
        # Chạy lệnh SQL lấy toàn bộ dữ liệu từ bảng tasks
        result = db.execute(text('SELECT * FROM tasks')).mappings().all()
        
        return {
            "status": "success",
            "message": "Lấy dữ liệu thành công!",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi lấy dữ liệu: {str(e)}"
        )