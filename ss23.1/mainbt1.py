from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
# Thêm JWTError để bắt các lỗi token
from jose import jwt, JWTError

app = FastAPI()

SECRET_KEY = "training-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

USERS = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Nguyen",
        "role": "user",
        "is_active": True,
    },
    "bob": {
        "username": "bob",
        "full_name": "Bob Tran",
        "role": "user",
        "is_active": False,
    },
}

@app.get("/issue-token/{username}")
def issue_token(username: str, expired: bool = False):
    if username not in USERS:
        raise HTTPException(status_code=404, detail="User not found")

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=-5 if expired else 30
    )

    token = jwt.encode(
        {
            "sub": username,
            "exp": expires_at,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


"""
===================================================================
PHẦN 1: PHÁT HIỆN LỖI (BUG DETECTION)
===================================================================
1. Dòng code gây lỗi ban đầu:
   - payload = jwt.get_unverified_claims(token)
   - Thiếu đoạn code kiểm tra if not user.get("is_active"):

2. Tại sao get_unverified_claims() không an toàn?
   - Hàm này chỉ đơn thuần giải mã (decode) payload mà KHÔNG kiểm tra 
     chữ ký (signature) và KHÔNG kiểm tra thời hạn (exp).
   - Hậu quả: Kẻ gian có thể sửa trường 'sub' để mạo danh người khác, 
     hoặc sử dụng lại token đã hết hạn từ lâu.

3. Test cases thực tế trên code cũ:
   - TC1 (Token hợp lệ): Mong đợi 200 OK -> Thực tế trả về 200 OK.
   - TC2 (Token hết hạn): Mong đợi 401 Unauthorized -> Thực tế trả về 200 OK (LỖI).
   - TC3 (Tài khoản bob bị khóa): Mong đợi 403 Forbidden -> Thực tế trả về 200 OK (LỖI).
===================================================================
PHẦN 2: SỬA SOURCE CODE (Bên dưới)
===================================================================
"""
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )
    
    try:
        # 1. Đã thay jwt.get_unverified_claims thành jwt.decode
        # Thao tác này tự động kiểm tra CHỮ KÝ và THỜI HẠN token.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        username = payload.get("sub")
        # 2. Kiểm tra xem token có chứa trường sub không
        if username is None:
            raise credentials_exception
            
    except JWTError:
        # Bắt các lỗi: Token hết hạn, sai chữ ký, token bị chỉnh sửa
        raise credentials_exception

    user = USERS.get(username)
    
    # 3. Kiểm tra người dùng có tồn tại trong hệ thống không
    if user is None:
        raise credentials_exception

    # 4. Kiểm tra chặn tài khoản đã bị khóa (is_active = False)
    if not user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user


@app.get("/users/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user