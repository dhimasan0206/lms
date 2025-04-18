import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Enum, ARRAY, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from domain.entities.user import UserRole, UserStatus
from domain.entities.token import TokenType
from domain.entities.oauth2_connection import OAuth2Provider

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=True)  # Nullable for OAuth users
    roles = Column(ARRAY(Enum(UserRole, name="user_role")), nullable=False, default=[])
    status = Column(Enum(UserStatus, name="user_status"), nullable=False, default=UserStatus.PENDING_VERIFICATION)
    organization_id = Column(UUID(as_uuid=True), nullable=True)
    branch_id = Column(UUID(as_uuid=True), nullable=True)
    profile_image_url = Column(String, nullable=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    phone_number = Column(String, nullable=True)
    email_verified = Column(Boolean, nullable=False, default=False)
    phone_verified = Column(Boolean, nullable=False, default=False)
    preferences = Column(JSON, nullable=False, default={})
    metadata = Column(JSON, nullable=False, default={})


class TokenModel(Base):
    __tablename__ = "tokens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_type = Column(Enum(TokenType, name="token_type"), nullable=False)
    token_value = Column(Text, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    revoked = Column(Boolean, nullable=False, default=False)
    revoked_at = Column(DateTime, nullable=True)
    device_info = Column(JSON, nullable=False, default={})
    metadata = Column(JSON, nullable=False, default={})


class OAuth2ConnectionModel(Base):
    __tablename__ = "oauth2_connections"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    provider = Column(Enum(OAuth2Provider, name="oauth2_provider"), nullable=False)
    provider_user_id = Column(String, nullable=False, index=True)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)
    profile_data = Column(JSON, nullable=False, default={})
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)
    
    __table_args__ = (
        # Unique constraint on provider and provider_user_id
        {"UniqueConstraint": ("provider", "provider_user_id", name="uq_oauth2_provider_user_id")},
    ) 