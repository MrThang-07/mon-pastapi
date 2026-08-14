import jwt
from datetime import datetime, timedelta, timezone

# SECRET_KEY: Trong thực tế, chuỗi này phải được giữ bí mật tuyệt đối và lưu trong file .env
SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_minutes: int) -> str:
    """
    Tạo Access Token với Payload và thời hạn cụ thể.
    """
    to_encode = data.copy()
    
    # Tính thời gian hết hạn (exp) chuẩn theo múi giờ UTC
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    
    # Thêm 'exp' vào payload
    to_encode.update({"exp": expire})
    
    # Mã hóa và ký JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Giải mã và kiểm tra tính hợp lệ của Access Token.
    """
    try:
        # jwt.decode sẽ tự động kiểm tra chữ ký (signature) và thời gian hết hạn (exp)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Xử lý ngoại lệ khi token đã quá hạn
        print("Lỗi: Token đã hết hạn (ExpiredSignatureError).")
        return None
    except jwt.InvalidTokenError:
        # Xử lý ngoại lệ khi token bị sai chữ ký hoặc cấu trúc không hợp lệ
        print("Lỗi: Token không hợp lệ (InvalidTokenError).")
        return None


# --- KIỂM THỬ (TESTING) ---
if __name__ == "__main__":
    # Dữ liệu không bao gồm mật khẩu
    payload_data = {
        "sub": "student01@gmail.com",
        "user_id": 1,
        "role": "student"
    }
    
    # Tạo Token
    token = create_access_token(data=payload_data, expires_minutes=30)
    print("Token:", token)
    
    # Giải mã Token
    print("\nKết quả giải mã hợp lệ:")
    decoded = decode_access_token(token)
    print(decoded)

# """
# --- 4. TRẢ LỜI CÂU HỎI BỔ SUNG ---

# Q1: Ba phần của JWT là gì?
# -> Gồm 3 phần cách nhau bởi dấu chấm: Header (thuật toán mã hóa), Payload (dữ liệu truyền tải), và Signature (chữ ký bảo mật).

# Q2: Payload của JWT có được mã hóa để che giấu dữ liệu hay không?
# -> KHÔNG. Payload chỉ được encode bằng Base64Url (ai cũng có thể decode và đọc được). Do đó, tuyệt đối không đưa thông tin nhạy cảm (như mật khẩu) vào Payload.

# Q3: Signature có vai trò gì?
# -> Đảm bảo tính toàn vẹn. Nó giúp server xác nhận token này do chính server tạo ra (nhờ SECRET_KEY) và nội dung bên trong chưa bị chỉnh sửa trên đường truyền.

# Q4: Điều gì xảy ra nếu người dùng tự sửa trường role trong Payload?
# -> Token sẽ trở nên không hợp lệ. Quá trình kiểm tra (decode) sẽ báo lỗi InvalidTokenError. Vì Signature được tạo dựa trên (Header + Payload + SECRET_KEY), nếu Payload bị sửa đổi, Signature tính lại sẽ không khớp với Signature cũ trong token.
# """