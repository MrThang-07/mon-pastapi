from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.core.config import settings

# Sử dụng HTTPBearer để tự động lấy token từ header "Authorization: Bearer <token>"
reusable_oauth2 = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(reusable_oauth2),
    db: Session = Depends(get_db)
) -> User:
    """
    Bác bảo vệ số 1: Kiểm tra tính hợp lệ của Token và lấy thông tin người dùng.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực thông tin đăng nhập!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Giải mã Token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại!"
        )
    except jwt.PyJWTError:
        raise credentials_exception

    # Truy vấn người dùng từ Database
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản này đã bị tạm khóa!"
        )

    return user

class RoleChecker:
    """
    Bác bảo vệ số 2: Phân quyền theo vai trò (Role-Based Access Control).
    """
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        # Vì role của bạn là kiểu chuỗi (VD: "USER", "ADMIN") lưu thẳng trong bảng User
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Quyền truy cập bị từ chối! Yêu cầu quyền: {self.allowed_roles}"
            )
        return current_user