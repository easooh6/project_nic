from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import bcrypt
from src.domain.repositories.user import IUserRepository
from src.domain.enums import RoleEnum
from src.infrastructure.db.models.user import User

class UserRepository(IUserRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_user(self, email: str, password: str, role: RoleEnum) -> User:
        """Create new user with unique email and hashed password"""
        existing_user = await self.get_by_email(email)
        if existing_user:
            raise ValueError("Email already exists")
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(
            email=email,
            password_hash=hashed_password,
            role=role,
            is_active=True
        )
        
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        
        return user
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by id"""
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_role(self, role: RoleEnum) -> List[User]:
        """Get users with specified role"""
        result = await self.session.execute(
            select(User).where(User.role == role)
        )
        return list(result.scalars().all())
    
    async def update_user(self, user_id: int, update_data: dict, is_admin: bool) -> Optional[User]:
        """Update user fields (only if is_admin=True)"""
        if not is_admin:
            raise PermissionError("Only admin can update users")
        
        user = await self.get_by_id(user_id)
        if not user:
            return None
        
        allowed_fields = ['email', 'password_hash', 'role', 'is_active']
        for field, value in update_data.items():
            if field in allowed_fields and hasattr(user, field):
                setattr(user, field, value)
        
        await self.session.commit()
        await self.session.refresh(user)
        
        return user
    
    async def delete_user(self, user_id: int) -> bool:
        """Delete user by id"""
        user = await self.get_by_id(user_id)
        if not user:
            return False
        
        await self.session.delete(user)
        await self.session.commit()
        
        return True