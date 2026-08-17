import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "123456789_khoa_bi_mat_rat_dai_va_an_toan_cho_jwt_devconnect"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str, cost_factor: int = 12) -> str:
    password_byte = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=cost_factor)
    hashed_password = bcrypt.hashpw(password_byte, salt)
    return hashed_password.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt