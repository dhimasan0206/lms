from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from domain.entities.token import Token, TokenType


class TokenRepository(ABC):
    @abstractmethod
    async def create(self, token: Token) -> Token:
        """Create a new token"""
        pass
    
    @abstractmethod
    async def get_by_id(self, token_id: UUID) -> Optional[Token]:
        """Get a token by ID"""
        pass
    
    @abstractmethod
    async def get_by_value(self, token_value: str) -> Optional[Token]:
        """Get a token by its value"""
        pass
    
    @abstractmethod
    async def get_active_by_user_and_type(self, user_id: UUID, token_type: TokenType) -> List[Token]:
        """Get active tokens for a user by token type"""
        pass
    
    @abstractmethod
    async def revoke(self, token_id: UUID) -> Token:
        """Revoke a token by ID"""
        pass
    
    @abstractmethod
    async def revoke_by_value(self, token_value: str) -> Token:
        """Revoke a token by its value"""
        pass
    
    @abstractmethod
    async def revoke_all_for_user(self, user_id: UUID, token_type: Optional[TokenType] = None) -> int:
        """Revoke all tokens for a user, optionally filtering by token type"""
        pass
    
    @abstractmethod
    async def is_token_valid(self, token_value: str) -> bool:
        """Check if a token is valid (exists, not expired, not revoked)"""
        pass
    
    @abstractmethod
    async def clean_expired_tokens(self, before_date: datetime) -> int:
        """Remove expired tokens from the database"""
        pass 