# RESEARCH GROUP MANAGEMENT API

Hệ thống Backend (FastAPI) quản lý Nhóm Nghiên cứu Khoa học. Cung cấp các API để quản lý người dùng, đề tài nghiên cứu, thành viên và tiến độ nhiệm vụ.

## Công nghệ sử dụng
* **Framework:** FastAPI
* **Database:** MySQL, SQLAlchemy (ORM)
* **Xác thực:** JWT (JSON Web Tokens), Passlib (Bcrypt)
* **Môi trường ảo:** venv

---

##  Hướng dẫn Cài đặt & Chạy dự án

### Bước 1: Tạo và kích hoạt môi trường ảo (Virtual Environment)
Mở Terminal tại thư mục gốc của dự án và chạy lệnh:
`python -m venv venv`
`venv\Scripts\activate`

### Bước 2: Cài đặt thư viện
`pip install -r requirements.txt`

### Bước 3: Cấu hình cơ sở dữ liệu (Database)
1. Mở MySQL, tạo một database rỗng: CREATE DATABASE research_management;
2. Copy file .env.example thành file mới đặt tên là .env.
3. Mở file .env và thay đổi thông tin kết nối DATABASE_URL theo đúng tài khoản MySQL trên máy của bạn.

### Bước 4: Khởi động Server
Chạy lệnh sau để khởi động FastAPI. Hệ thống sẽ tự động tạo các bảng trong Database nếu chưa có:
`uvicorn app.main:app --reload`

### Bước 5: Kiểm tra và sử dụng
* API Health Check: http://127.0.0.1:8000/health-check
* Swagger UI (Tài liệu API tự động): http://127.0.0.1:8000/docs