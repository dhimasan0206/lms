from pydantic import BaseModel, Field, UUID4
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class OAuth2Provider(str, Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"
    GITHUB = "github"
    APPLE = "apple"


class OAuth2Connection(BaseModel):
    id: UUID4
    user_id: UUID4
    provider: OAuth2Provider
    provider_user_id: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None
    profile_data: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
    last_used_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 