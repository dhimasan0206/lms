from pydantic import BaseModel, EmailStr, Field, UUID4, validator
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

from domain.entities.user import UserRole, UserStatus
from domain.entities.oauth2_connection import OAuth2Provider


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    device_name: Optional[str] = None
    device_info: Optional[Dict[str, Any]] = None


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    first_name: str
    last_name: str
    username: Optional[str] = None
    organization_id: Optional[UUID4] = None
    branch_id: Optional[UUID4] = None
    phone_number: Optional[str] = None
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


class SocialLoginRequest(BaseModel):
    provider: OAuth2Provider
    access_token: str
    device_name: Optional[str] = None
    device_info: Optional[Dict[str, Any]] = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class ConfirmResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class VerifyEmailRequest(BaseModel):
    token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    id: UUID4
    email: EmailStr
    username: Optional[str] = None
    first_name: str
    last_name: str
    roles: List[UserRole]
    status: UserStatus
    organization_id: Optional[UUID4] = None
    branch_id: Optional[UUID4] = None
    profile_image_url: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    email_verified: bool
    phone_number: Optional[str] = None
    phone_verified: bool
    
    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    user: UserResponse
    token: TokenResponse


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class UpdateUserProfileRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    profile_image_url: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None 