import os
from typing import List
from pydantic import BaseSettings, validator
from pydantic.networks import AnyHttpUrl


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "LMS API Gateway"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS settings
    CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[AnyHttpUrl]:
        if isinstance(v, str) and not v.startswith("["):
            return [v]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Service URLs
    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    USER_SERVICE_URL: str = "http://user-service:8002"
    COURSE_SERVICE_URL: str = "http://course-service:8003"
    CONTENT_SERVICE_URL: str = "http://content-service:8004"
    ENROLLMENT_SERVICE_URL: str = "http://enrollment-service:8005"
    ASSESSMENT_SERVICE_URL: str = "http://assessment-service:8006"
    BADGE_SERVICE_URL: str = "http://badge-service:8007"
    ANALYTICS_SERVICE_URL: str = "http://analytics-service:8008"
    NOTIFICATION_SERVICE_URL: str = "http://notification-service:8009"
    
    # JWT settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis settings
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings() 