from pydantic import BaseModel, EmailStr, Field, UUID4
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ORGANIZATION_ADMIN = "organization_admin"
    BRANCH_MANAGER = "branch_manager"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING_VERIFICATION = "pending_verification"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class User(BaseModel):
    id: UUID4
    email: EmailStr
    username: Optional[str] = None
    first_name: str
    last_name: str
    password_hash: str
    roles: List[UserRole]
    status: UserStatus
    organization_id: Optional[UUID4] = None
    branch_id: Optional[UUID4] = None
    profile_image_url: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    phone_number: Optional[str] = None
    email_verified: bool = False
    phone_verified: bool = False
    preferences: dict = Field(default_factory=dict)
    metadata: dict = Field(default_factory=dict)
    
    class Config:
        from_attributes = True 