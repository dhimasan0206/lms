from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.user import User, UserStatus


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user"""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by ID"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email address"""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update an existing user"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Delete a user by ID"""
        pass
    
    @abstractmethod
    async def list_by_organization(self, organization_id: UUID, offset: int = 0, limit: int = 100) -> List[User]:
        """List users by organization ID"""
        pass
    
    @abstractmethod
    async def list_by_branch(self, branch_id: UUID, offset: int = 0, limit: int = 100) -> List[User]:
        """List users by branch ID"""
        pass
    
    @abstractmethod
    async def update_status(self, user_id: UUID, status: UserStatus) -> User:
        """Update a user's status"""
        pass
    
    @abstractmethod
    async def verify_email(self, user_id: UUID) -> User:
        """Mark a user's email as verified"""
        pass
    
    @abstractmethod
    async def update_password(self, user_id: UUID, password_hash: str) -> User:
        """Update a user's password hash"""
        pass
    
    @abstractmethod
    async def update_last_login(self, user_id: UUID) -> User:
        """Update a user's last login timestamp"""
        pass 