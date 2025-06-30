from pydantic_settings import BaseSettings
from typing import List
import json
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Zenith Study Buddy"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database - SQLite as default
    DATABASE_URL: str = "sqlite:///./zenith_study_buddy.db"
    # For async SQLite (optional):
    # DATABASE_URL: str = "sqlite+aiosqlite:///./zenith_study_buddy.db"
    
    # Alternative free databases:
    # MySQL: DATABASE_URL: str = "mysql://root:password@localhost/zenith"
    # MariaDB: DATABASE_URL: str = "mariadb://root:password@localhost/zenith"
    
    # Redis (optional)
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "3e723a6b65044f9fa24880f6f986e36b")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Omnidim
    OMNIDIM_API_KEY: str = os.getenv("OMNIDIM_API_KEY", "kPF7HWuHOg11w14qQDUwSfxEp1mvu1tIABAV9M-OIJw")
    OMNIDIM_API_URL: str = "https://api.omnidim.io/v1"
    OMNIDIM_WS_URL: str = "wss://ws.omnidim.io"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
    @property
    def cors_origins_list(self):
        if isinstance(self.CORS_ORIGINS, str):
            return json.loads(self.CORS_ORIGINS)
        return self.CORS_ORIGINS

settings = Settings()
