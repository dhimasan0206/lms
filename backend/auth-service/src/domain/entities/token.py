from pydantic import BaseModel, Field, UUID4
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    RESET_PASSWORD = "reset_password"
    EMAIL_VERIFICATION = "email_verification"
    API_KEY = "api_key"


class Token(BaseModel):
    id: UUID4
    user_id: UUID4
    token_type: TokenType
    token_value: str
    expires_at: datetime
    created_at: datetime
    revoked: bool = False
    revoked_at: Optional[datetime] = None
    device_info: Optional[Dict[str, Any]] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        from_attributes = True 