import os
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("MEDCARE_SECRET_KEY", "fallback_secret_key")
ALGORITHM = "HS256"

app = FastAPI(title="MedCare E-Prescription System", version="1.0.0")
security = HTTPBearer()

# Database giả lập trên RAM để code chạy ngay không cần cài MySQL
fake_users_db = []

# --- SCHEMAS ---
class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str = Field(..., description="Chỉ nhận 'doctor' hoặc 'pharmacist'")

class LoginRequest(BaseModel):
    username: str
    password: str

class PrescriptionCreate(BaseModel):
    patient_name: str
    diagnosis: str
    medicine: str

# --- UTILS (Bcrypt & JWT) ---
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=20) # Hết hạn sau 20 phút
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- DEPENDENCY XÁC THỰC TOKEN & PHÂN QUYỀN ---
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Trả về payload chứa {"sub": username, "role": role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token đã hết hạn")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ hoặc chữ ký bị sai")

# --- API ENDPOINTS ---

@app.post("/api/v1/medical/register", status_code=201)
def register(user: RegisterRequest):
    if user.role not in ["doctor", "pharmacist"]:
        raise HTTPException(status_code=400, detail="Role phải là 'doctor' hoặc 'pharmacist'")
    
    # Kiểm tra trùng username
    for u in fake_users_db:
        if u["username"] == user.username:
            raise HTTPException(status_code=400, detail="Tài khoản đã tồn tại")
            
    hashed_pwd = hash_password(user.password)
    fake_users_db.append({
        "username": user.username,
        "password": hashed_pwd,
        "role": user.role
    })
    return {"message": "Đăng ký thành công", "username": user.username, "role": user.role}

@app.post("/api/v1/medical/login")
def login(user: LoginRequest):
    db_user = None
    for u in fake_users_db:
        if u["username"] == user.username:
            db_user = u
            break
            
    # Thông báo lỗi chung chung để bảo mật
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Thông tin đăng nhập không chính xác")
        
    # Tạo token chứa role
    token = create_access_token({"sub": db_user["username"], "role": db_user["role"]})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/v1/prescriptions")
def create_prescription(prescription: PrescriptionCreate, current_user: dict = Depends(get_current_user)):
    # Yêu cầu: Chỉ bác sĩ mới được tạo đơn thuốc
    if current_user.get("role") != "doctor":
        raise HTTPException(status_code=403, detail="Không đủ quyền hạn (Chỉ Bác sĩ mới được tạo đơn thuốc)")
    return {
        "message": "Tạo đơn thuốc thành công",
        "doctor": current_user.get("sub"),
        "data": prescription
    }

@app.get("/api/v1/prescriptions/view")
def view_prescriptions(current_user: dict = Depends(get_current_user)):
    # Yêu cầu: Cả bác sĩ và dược sĩ đều được xem
    return {
        "message": "Danh sách đơn thuốc",
        "user": current_user.get("sub"),
        "role": current_user.get("role"),
        "prescriptions": [
            {"id": 1, "patient": "Nguyễn Văn A", "medicine": "Paracetamol 500mg"},
            {"id": 2, "patient": "Trần Thị B", "medicine": "Amoxicillin 250mg"}
        ]
    }