from typing import Optional, List
from sqlalchemy import select
from src.domain.enums import RoleEnum
from src.infrastructure.db.models.user import User
from src.infrastructure.db.db import get_db_session


class UserRepository:
    
    def __init__(self):
        self.session_factory = get_db_session()
    
    async def create_user(self, email: str, password_hash: str, role: RoleEnum) -> User:
        async with self.session_factory() as session:
            # Check if user already exists
            existing_user = await self.get_by_email(email)
            if existing_user:
                raise ValueError("Email already exists")
            
            user = User(
                email=email,
                password_hash=password_hash,
                role=role,
                is_active=True
            )
            
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
            return user
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(User).where(User.email == email)
            )
            return result.scalar_one_or_none()
    
    async def get_by_role(self, role: RoleEnum) -> List[User]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(User).where(User.role == role)
            )
            return list(result.scalars().all())
    
    async def get_all(self) -> List[User]:
        async with self.session_factory() as session:
            result = await session.execute(select(User))
            return list(result.scalars().all())
    
    async def update_user(self, user_id: int, update_data: dict) -> Optional[User]:
        async with self.session_factory() as session:
            user = await session.get(User, user_id)
            if not user:
                return None
            
            allowed_fields = ['email', 'password_hash', 'role', 'is_active']
            for field, value in update_data.items():
                if field in allowed_fields and hasattr(user, field):
                    setattr(user, field, value)
            
            await session.commit()
            await session.refresh(user)
            
            return user
    
    async def delete_user(self, user_id: int) -> bool:
        async with self.session_factory() as session:
            user = await session.get(User, user_id)
            if not user:
                return False
            
            await session.delete(user)
            await session.commit()
            
            return True