from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Research Group Management API"
    
    # Cấu hình Database
    DATABASE_URL: str
    
    # Cấu hình JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()