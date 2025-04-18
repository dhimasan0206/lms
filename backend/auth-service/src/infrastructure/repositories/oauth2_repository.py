from uuid import UUID
from typing import List, Optional
from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.oauth2_connection import OAuth2Connection, OAuth2Provider
from domain.repositories.oauth2_repository import OAuth2Repository
from infrastructure.database.models import OAuth2ConnectionModel


class SQLAlchemyOAuth2Repository(OAuth2Repository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, oauth2_connection: OAuth2Connection) -> OAuth2Connection:
        """Create a new OAuth2 connection"""
        connection_model = OAuth2ConnectionModel(
            id=oauth2_connection.id,
            user_id=oauth2_connection.user_id,
            provider=oauth2_connection.provider,
            provider_user_id=oauth2_connection.provider_user_id,
            access_token=oauth2_connection.access_token,
            refresh_token=oauth2_connection.refresh_token,
            token_expires_at=oauth2_connection.token_expires_at,
            profile_data=oauth2_connection.profile_data,
            created_at=oauth2_connection.created_at,
            updated_at=oauth2_connection.updated_at,
            last_used_at=oauth2_connection.last_used_at
        )
        
        self.session.add(connection_model)
        await self.session.flush()
        await self.session.refresh(connection_model)
        
        return OAuth2Connection.model_validate(connection_model)
    
    async def get_by_id(self, connection_id: UUID) -> Optional[OAuth2Connection]:
        """Get an OAuth2 connection by ID"""
        result = await self.session.execute(
            select(OAuth2ConnectionModel).where(OAuth2ConnectionModel.id == connection_id)
        )
        connection_model = result.scalars().first()
        
        if not connection_model:
            return None
        
        return OAuth2Connection.model_validate(connection_model)
    
    async def get_by_user_and_provider(self, user_id: UUID, provider: OAuth2Provider) -> Optional[OAuth2Connection]:
        """Get an OAuth2 connection by user ID and provider"""
        result = await self.session.execute(
            select(OAuth2ConnectionModel).where(
                OAuth2ConnectionModel.user_id == user_id,
                OAuth2ConnectionModel.provider == provider
            )
        )
        connection_model = result.scalars().first()
        
        if not connection_model:
            return None
        
        return OAuth2Connection.model_validate(connection_model)
    
    async def get_by_provider_user_id(self, provider: OAuth2Provider, provider_user_id: str) -> Optional[OAuth2Connection]:
        """Get an OAuth2 connection by provider and provider's user ID"""
        result = await self.session.execute(
            select(OAuth2ConnectionModel).where(
                OAuth2ConnectionModel.provider == provider,
                OAuth2ConnectionModel.provider_user_id == provider_user_id
            )
        )
        connection_model = result.scalars().first()
        
        if not connection_model:
            return None
        
        return OAuth2Connection.model_validate(connection_model)
    
    async def update(self, oauth2_connection: OAuth2Connection) -> OAuth2Connection:
        """Update an existing OAuth2 connection"""
        await self.session.execute(
            update(OAuth2ConnectionModel)
            .where(OAuth2ConnectionModel.id == oauth2_connection.id)
            .values(
                user_id=oauth2_connection.user_id,
                provider=oauth2_connection.provider,
                provider_user_id=oauth2_connection.provider_user_id,
                access_token=oauth2_connection.access_token,
                refresh_token=oauth2_connection.refresh_token,
                token_expires_at=oauth2_connection.token_expires_at,
                profile_data=oauth2_connection.profile_data,
                updated_at=datetime.utcnow(),
                last_used_at=oauth2_connection.last_used_at
            )
        )
        
        return await self.get_by_id(oauth2_connection.id)
    
    async def delete(self, connection_id: UUID) -> bool:
        """Delete an OAuth2 connection"""
        result = await self.session.execute(
            delete(OAuth2ConnectionModel).where(OAuth2ConnectionModel.id == connection_id)
        )
        return result.rowcount > 0
    
    async def list_by_user(self, user_id: UUID) -> List[OAuth2Connection]:
        """List all OAuth2 connections for a user"""
        result = await self.session.execute(
            select(OAuth2ConnectionModel).where(OAuth2ConnectionModel.user_id == user_id)
        )
        connection_models = result.scalars().all()
        
        return [OAuth2Connection.model_validate(model) for model in connection_models]
    
    async def update_tokens(self, connection_id: UUID, access_token: str, refresh_token: Optional[str], expires_at: Optional[str]) -> OAuth2Connection:
        """Update tokens for an OAuth2 connection"""
        # Get existing connection
        connection = await self.get_by_id(connection_id)
        if not connection:
            return None
        
        # Update fields
        values = {
            "access_token": access_token,
            "updated_at": datetime.utcnow(),
            "last_used_at": datetime.utcnow()
        }
        
        if refresh_token:
            values["refresh_token"] = refresh_token
        
        if expires_at:
            values["token_expires_at"] = expires_at
        
        # Execute update
        await self.session.execute(
            update(OAuth2ConnectionModel)
            .where(OAuth2ConnectionModel.id == connection_id)
            .values(**values)
        )
        
        return await self.get_by_id(connection_id) 