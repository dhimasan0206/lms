from uuid import UUID
from typing import List, Optional
from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user import User, UserStatus
from domain.repositories.user_repository import UserRepository
from infrastructure.database.models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user: User) -> User:
        """Create a new user"""
        user_model = UserModel(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            password_hash=user.password_hash,
            roles=user.roles,
            status=user.status,
            organization_id=user.organization_id,
            branch_id=user.branch_id,
            profile_image_url=user.profile_image_url,
            last_login=user.last_login,
            created_at=user.created_at,
            updated_at=user.updated_at,
            phone_number=user.phone_number,
            email_verified=user.email_verified,
            phone_verified=user.phone_verified,
            preferences=user.preferences,
            metadata=user.metadata
        )
        
        self.session.add(user_model)
        await self.session.flush()
        await self.session.refresh(user_model)
        
        return User.model_validate(user_model)
    
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by ID"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalars().first()
        
        if not user_model:
            return None
        
        return User.model_validate(user_model)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email address"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_model = result.scalars().first()
        
        if not user_model:
            return None
        
        return User.model_validate(user_model)
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        user_model = result.scalars().first()
        
        if not user_model:
            return None
        
        return User.model_validate(user_model)
    
    async def update(self, user: User) -> User:
        """Update an existing user"""
        await self.session.execute(
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                password_hash=user.password_hash,
                roles=user.roles,
                status=user.status,
                organization_id=user.organization_id,
                branch_id=user.branch_id,
                profile_image_url=user.profile_image_url,
                last_login=user.last_login,
                updated_at=datetime.utcnow(),
                phone_number=user.phone_number,
                email_verified=user.email_verified,
                phone_verified=user.phone_verified,
                preferences=user.preferences,
                metadata=user.metadata
            )
        )
        
        # Fetch the updated user
        return await self.get_by_id(user.id)
    
    async def delete(self, user_id: UUID) -> bool:
        """Delete a user by ID"""
        result = await self.session.execute(
            delete(UserModel).where(UserModel.id == user_id)
        )
        return result.rowcount > 0
    
    async def list_by_organization(self, organization_id: UUID, offset: int = 0, limit: int = 100) -> List[User]:
        """List users by organization ID"""
        result = await self.session.execute(
            select(UserModel)
            .where(UserModel.organization_id == organization_id)
            .offset(offset)
            .limit(limit)
        )
        user_models = result.scalars().all()
        
        return [User.model_validate(user_model) for user_model in user_models]
    
    async def list_by_branch(self, branch_id: UUID, offset: int = 0, limit: int = 100) -> List[User]:
        """List users by branch ID"""
        result = await self.session.execute(
            select(UserModel)
            .where(UserModel.branch_id == branch_id)
            .offset(offset)
            .limit(limit)
        )
        user_models = result.scalars().all()
        
        return [User.model_validate(user_model) for user_model in user_models]
    
    async def update_status(self, user_id: UUID, status: UserStatus) -> User:
        """Update a user's status"""
        await self.session.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(
                status=status,
                updated_at=datetime.utcnow()
            )
        )
        
        return await self.get_by_id(user_id)
    
    async def verify_email(self, user_id: UUID) -> User:
        """Mark a user's email as verified"""
        await self.session.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(
                email_verified=True,
                updated_at=datetime.utcnow()
            )
        )
        
        return await self.get_by_id(user_id)
    
    async def update_password(self, user_id: UUID, password_hash: str) -> User:
        """Update a user's password hash"""
        await self.session.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(
                password_hash=password_hash,
                updated_at=datetime.utcnow()
            )
        )
        
        return await self.get_by_id(user_id)
    
    async def update_last_login(self, user_id: UUID) -> User:
        """Update a user's last login timestamp"""
        await self.session.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(
                last_login=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        )
        
        return await self.get_by_id(user_id) 