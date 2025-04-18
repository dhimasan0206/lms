from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import uuid

from config.settings import Settings
from infrastructure.database.connection import Database
from infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from infrastructure.repositories.token_repository import SQLAlchemyTokenRepository
from infrastructure.repositories.oauth2_repository import SQLAlchemyOAuth2Repository
from application.services.auth_service import AuthService
from application.services.oauth2_service import OAuth2Service
from domain.entities.user import UserRole

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
    description="JWT token authentication",
    auto_error=False
)

# Initialize settings and database
settings = Settings()
db = Database(settings)


async def get_db_session() -> AsyncSession:
    """Get a database session"""
    async with db.session() as session:
        yield session


async def get_user_repository(session: AsyncSession = Depends(get_db_session)):
    """Get a user repository"""
    return SQLAlchemyUserRepository(session)


async def get_token_repository(session: AsyncSession = Depends(get_db_session)):
    """Get a token repository"""
    return SQLAlchemyTokenRepository(session)


async def get_oauth2_repository(session: AsyncSession = Depends(get_db_session)):
    """Get an OAuth2 repository"""
    return SQLAlchemyOAuth2Repository(session)


async def get_auth_service(
    user_repository=Depends(get_user_repository),
    token_repository=Depends(get_token_repository)
):
    """Get an authentication service"""
    return AuthService(user_repository, token_repository, settings)


async def get_oauth2_service(
    user_repository=Depends(get_user_repository),
    oauth2_repository=Depends(get_oauth2_repository),
    auth_service=Depends(get_auth_service)
):
    """Get an OAuth2 service"""
    return OAuth2Service(user_repository, oauth2_repository, auth_service, settings)


async def get_current_user_id(
    token: Optional[str] = Depends(oauth2_scheme),
    token_repository=Depends(get_token_repository)
) -> Optional[uuid.UUID]:
    """Get the current user's ID from the access token"""
    if not token:
        return None
    
    try:
        # Decode token
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Check token type
        if payload.get("type") != "access":
            return None
        
        # Get user ID
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        return uuid.UUID(user_id)
    except (JWTError, ValueError):
        return None


async def get_current_user(
    user_id: Optional[uuid.UUID] = Depends(get_current_user_id),
    user_repository=Depends(get_user_repository)
):
    """Get the current user"""
    if not user_id:
        return None
    
    return await user_repository.get_by_id(user_id)


async def require_authenticated(
    user = Depends(get_current_user)
):
    """Require an authenticated user"""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def require_roles(
    required_roles: List[UserRole],
    user = Depends(require_authenticated)
):
    """Require specific roles"""
    for role in required_roles:
        if role in user.roles:
            return user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions",
    ) 