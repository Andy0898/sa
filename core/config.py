from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Chat API"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "FastAPI backend for AI chat application"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    ALLOWED_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    
    # Database
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "Abcd1234"
    MYSQL_DB: str = "sadb"
    DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    
    # Milvus
    MILVUS_HOST: str = os.getenv("MILVUS_HOST", "localhost")
    MILVUS_PORT: int = int(os.getenv("MILVUS_PORT", "19530"))
    
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    
    class Config:
        case_sensitive = True

settings = Settings() 