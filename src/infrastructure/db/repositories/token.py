from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, delete
from src.infrastructure.db.models.refresh_token import RefreshToken
from src.infrastructure.db.db import get_db_session


class RefreshTokenRepository:
    
    def __init__(self):
        self.session_factory = get_db_session
    
    async def create_token(self, token: str, user_id: int, expires_at: datetime) -> RefreshToken:
        async with self.session_factory() as session:
            refresh_token = RefreshToken(
                user_id=user_id,
                token=token,
                expires_at=expires_at,
                revoked=False
            )
            
            session.add(refresh_token)
            await session.commit()
            await session.refresh(refresh_token)
            
            return refresh_token
    
    async def get_by_user_id(self, user_id: int) -> List[RefreshToken]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(RefreshToken).where(RefreshToken.user_id == user_id)
            )
            return list(result.scalars().all())
    
    async def get_by_token(self, token: str) -> Optional[RefreshToken]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(RefreshToken).where(RefreshToken.token == token)
            )
            return result.scalar_one_or_none()
    
    async def get_all(self) -> List[RefreshToken]:
        async with self.session_factory() as session:
            result = await session.execute(select(RefreshToken))
            return list(result.scalars().all())
    
    async def get_active_tokens(self) -> List[RefreshToken]:
        async with self.session_factory() as session:
            now = datetime.utcnow()
            result = await session.execute(
                select(RefreshToken).where(
                    RefreshToken.revoked == False,
                    RefreshToken.expires_at > now
                )
            )
            return list(result.scalars().all())
    
    async def revoke_token(self, token: str) -> bool:
        async with self.session_factory() as session:
            refresh_token_result = await session.execute(
                select(RefreshToken).where(RefreshToken.token == token)
            )
            refresh_token = refresh_token_result.scalar_one_or_none()
            
            if not refresh_token:
                return False
            
            refresh_token.revoked = True
            await session.commit()
            
            return True
    
    async def delete_expired_tokens(self) -> int:
        async with self.session_factory() as session:
            now = datetime.utcnow()
            result = await session.execute(
                delete(RefreshToken).where(RefreshToken.expires_at < now)
            )
            await session.commit()
            
            return result.rowcount