from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Zenith Study Buddy"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Omnidim
    OMNIDIM_API_KEY: str
    OMNIDIM_API_URL: str = "https://api.omnidim.io/v1"
    OMNIDIM_WS_URL: str = "wss://ws.omnidim.io"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        
    @property
    def cors_origins_list(self):
        if isinstance(self.CORS_ORIGINS, str):
            return json.loads(self.CORS_ORIGINS)
        return self.CORS_ORIGINS

settings = Settings()