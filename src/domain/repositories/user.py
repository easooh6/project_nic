from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from src.domain.enums import RoleEnum
from src.infrastructure.db.models.user import User

class IUserRepository(ABC):
    
    @abstractmethod
    async def create_user(self, email: str, password: str, role: RoleEnum) -> User:
        """Create new user with unique email and hashed password"""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by id"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass
    
    @abstractmethod
    async def get_by_role(self, role: RoleEnum) -> List[User]:
        """Get users with specified role"""
        pass
    
    @abstractmethod
    async def update_user(self, user_id: int, update_data: dict, is_admin: bool) -> Optional[User]:
        """Update user fields (only if is_admin=True)"""
        pass
    
    @abstractmethod
    async def delete_user(self, user_id: int) -> bool:
        """Delete user by id"""
        pass