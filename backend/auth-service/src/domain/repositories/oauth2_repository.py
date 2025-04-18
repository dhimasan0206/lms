from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.oauth2_connection import OAuth2Connection, OAuth2Provider


class OAuth2Repository(ABC):
    @abstractmethod
    async def create(self, oauth2_connection: OAuth2Connection) -> OAuth2Connection:
        """Create a new OAuth2 connection"""
        pass
    
    @abstractmethod
    async def get_by_id(self, connection_id: UUID) -> Optional[OAuth2Connection]:
        """Get an OAuth2 connection by ID"""
        pass
    
    @abstractmethod
    async def get_by_user_and_provider(self, user_id: UUID, provider: OAuth2Provider) -> Optional[OAuth2Connection]:
        """Get an OAuth2 connection by user ID and provider"""
        pass
    
    @abstractmethod
    async def get_by_provider_user_id(self, provider: OAuth2Provider, provider_user_id: str) -> Optional[OAuth2Connection]:
        """Get an OAuth2 connection by provider and provider's user ID"""
        pass
    
    @abstractmethod
    async def update(self, oauth2_connection: OAuth2Connection) -> OAuth2Connection:
        """Update an existing OAuth2 connection"""
        pass
    
    @abstractmethod
    async def delete(self, connection_id: UUID) -> bool:
        """Delete an OAuth2 connection"""
        pass
    
    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> List[OAuth2Connection]:
        """List all OAuth2 connections for a user"""
        pass
    
    @abstractmethod
    async def update_tokens(self, connection_id: UUID, access_token: str, refresh_token: Optional[str], expires_at: Optional[str]) -> OAuth2Connection:
        """Update tokens for an OAuth2 connection"""
        pass 