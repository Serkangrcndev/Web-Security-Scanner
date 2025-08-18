from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Base directory
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Database
    DATABASE_URL: str = "mssql+pyodbc://sa:YourStrong@Passw0rd@localhost:1433/security_scanner?driver=ODBC+Driver+17+for+SQL+Server"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Keys
    SHODAN_API_KEY: Optional[str] = None
    NUCLEI_API_KEY: Optional[str] = None
    
    # Security
    CORS_ORIGINS: list = ["http://localhost:3000"]
    
    # Premium Features
    FREE_SCAN_LIMIT: int = 10
    PREMIUM_SCAN_LIMIT: int = 100
    
    # Scanner Settings
    SCAN_TIMEOUT: int = 300  # 5 minutes
    MAX_CONCURRENT_SCANS: int = 5
    
    class Config:
        env_file = ".env"

settings = Settings()
