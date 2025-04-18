from uuid import UUID
from typing import List, Optional
from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.token import Token, TokenType
from domain.repositories.token_repository import TokenRepository
from infrastructure.database.models import TokenModel


class SQLAlchemyTokenRepository(TokenRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, token: Token) -> Token:
        """Create a new token"""
        token_model = TokenModel(
            id=token.id,
            user_id=token.user_id,
            token_type=token.token_type,
            token_value=token.token_value,
            expires_at=token.expires_at,
            created_at=token.created_at,
            revoked=token.revoked,
            revoked_at=token.revoked_at,
            device_info=token.device_info,
            metadata=token.metadata
        )
        
        self.session.add(token_model)
        await self.session.flush()
        await self.session.refresh(token_model)
        
        return Token.model_validate(token_model)
    
    async def get_by_id(self, token_id: UUID) -> Optional[Token]:
        """Get a token by ID"""
        result = await self.session.execute(
            select(TokenModel).where(TokenModel.id == token_id)
        )
        token_model = result.scalars().first()
        
        if not token_model:
            return None
        
        return Token.model_validate(token_model)
    
    async def get_by_value(self, token_value: str) -> Optional[Token]:
        """Get a token by its value"""
        result = await self.session.execute(
            select(TokenModel).where(TokenModel.token_value == token_value)
        )
        token_model = result.scalars().first()
        
        if not token_model:
            return None
        
        return Token.model_validate(token_model)
    
    async def get_active_by_user_and_type(self, user_id: UUID, token_type: TokenType) -> List[Token]:
        """Get active tokens for a user by token type"""
        result = await self.session.execute(
            select(TokenModel)
            .where(
                TokenModel.user_id == user_id,
                TokenModel.token_type == token_type,
                TokenModel.revoked == False,
                TokenModel.expires_at > datetime.utcnow()
            )
        )
        token_models = result.scalars().all()
        
        return [Token.model_validate(token_model) for token_model in token_models]
    
    async def revoke(self, token_id: UUID) -> Token:
        """Revoke a token by ID"""
        await self.session.execute(
            update(TokenModel)
            .where(TokenModel.id == token_id)
            .values(
                revoked=True,
                revoked_at=datetime.utcnow()
            )
        )
        
        return await self.get_by_id(token_id)
    
    async def revoke_by_value(self, token_value: str) -> Token:
        """Revoke a token by its value"""
        token = await self.get_by_value(token_value)
        if not token:
            return None
        
        return await self.revoke(token.id)
    
    async def revoke_all_for_user(self, user_id: UUID, token_type: Optional[TokenType] = None) -> int:
        """Revoke all tokens for a user, optionally filtering by token type"""
        query = update(TokenModel).where(
            TokenModel.user_id == user_id,
            TokenModel.revoked == False
        )
        
        if token_type:
            query = query.where(TokenModel.token_type == token_type)
        
        result = await self.session.execute(
            query.values(
                revoked=True,
                revoked_at=datetime.utcnow()
            )
        )
        
        return result.rowcount
    
    async def is_token_valid(self, token_value: str) -> bool:
        """Check if a token is valid (exists, not expired, not revoked)"""
        result = await self.session.execute(
            select(TokenModel).where(
                TokenModel.token_value == token_value,
                TokenModel.revoked == False,
                TokenModel.expires_at > datetime.utcnow()
            )
        )
        token_model = result.scalars().first()
        
        return token_model is not None
    
    async def clean_expired_tokens(self, before_date: datetime) -> int:
        """Remove expired tokens from the database"""
        result = await self.session.execute(
            delete(TokenModel).where(
                TokenModel.expires_at < before_date
            )
        )
        
        return result.rowcount 