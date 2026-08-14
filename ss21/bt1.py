import bcrypt

def hash_password(password: str) -> str:
    """
    Nhận mật khẩu gốc và trả về mật khẩu đã băm bằng Bcrypt.
    """
    # bcrypt yêu cầu dữ liệu đầu vào là kiểu bytes, nên cần encode string sang utf-8
    password_bytes = password.encode('utf-8')
    
    # Tạo salt ngẫu nhiên
    salt = bcrypt.gensalt()
    
    # Băm mật khẩu với salt
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # Chuyển đổi lại thành string để lưu trữ dễ dàng
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Kiểm tra mật khẩu người dùng nhập vào có khớp với mật khẩu đã băm hay không.
    """
    # Encode cả mật khẩu nhập vào và chuỗi hash trong DB về dạng bytes
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    # Hàm checkpw sẽ tự động trích xuất salt từ chuỗi hash và so sánh
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)


# --- KIỂM THỬ (TESTING) ---
if __name__ == "__main__":
    password = "Rikkei@123"
    
    # Băm mật khẩu
    hashed_password = hash_password(password)
    print(hashed_password)  # Sẽ in ra chuỗi có dạng $2b$12$...
    
    # Kiểm tra mật khẩu đúng
    print(verify_password("Rikkei@123", hashed_password))  # Mong đợi: True
    
    # Kiểm tra mật khẩu sai
    print(verify_password("Rikkei@456", hashed_password))  # Mong đợi: False

    # """
# --- 4. TRẢ LỜI CÂU HỎI BỔ SUNG ---

# Q1: Vì sao không nên lưu mật khẩu trực tiếp vào database?
# -> Tránh lộ mật khẩu gốc khi database bị hack. Tránh rủi ro cho người dùng vì họ thường dùng chung 1 mật khẩu cho nhiều tài khoản khác (ngân hàng, email...).

# Q2: Vì sao cùng một mật khẩu nhưng hai lần băm có thể tạo ra hai chuỗi hash khác nhau?
# -> Do Bcrypt tự động sinh ra một chuỗi `Salt` ngẫu nhiên cho mỗi lần băm (Quá trình băm = Mật khẩu + Salt ngẫu nhiên).

# Q3: Salt có tác dụng gì trong việc chống Rainbow Table?
# -> Làm vô hiệu hóa Rainbow Table (bảng chứa các chuỗi hash tính sẵn). Vì mỗi user có Salt khác nhau, hacker phải tạo lại bảng hash từ đầu cho từng Salt rất tốn thời gian và tài nguyên.
# """