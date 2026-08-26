from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import jwt

from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services import user as user_service 
from app.core.security import create_access_token

from app.core.config import settings 
from app.models.user import User 

router = APIRouter(
    prefix="/auth", # Đường dẫn gốc cho các API trong file này
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    API Đăng ký tài khoản mới:
    - Nhận dữ liệu đầu vào (user_data) từ Request.
    - Gọi service để xử lý logic lưu DB.
    - Trả về thông tin an toàn (UserResponse).
    """
    new_user = user_service.create_user(db=db, user_data=user_data)
    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    API Đăng nhập:
    - Xác thực thông tin.
    - Trả về mã Token (vé thông hành) và Refresh Token.
    """
    user = user_service.authenticate_user(db=db, user_data=user_data)

    # Lấy quyền của user. 
    role_name = user.role 
    token_data = {"sub": user.email, "id": user.id, "role": role_name}
    
    # 1. Tạo JWT Access Token
    access_token = create_access_token(data=token_data)

    # # 2. Tạo JWT Refresh Token (Vé dài hạn) 
    # refresh_token = create_refresh_token(data=token_data)

    return {
        "message": "Đăng nhập thành công",
        "access_token": access_token,
        # "refresh_token": refresh_token,
        "token_type": "bearer",
        "data": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": role_name,
            "is_active": user.is_active
        }
    }

