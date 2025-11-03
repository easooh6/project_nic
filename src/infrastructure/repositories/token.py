from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from src.domain.repositories.token import IRefreshTokenRepository
from src.infrastructure.db.models.refresh_token import RefreshToken

class RefreshTokenRepository(IRefreshTokenRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_token(self, token: str, user_id: int, expires_at: datetime) -> RefreshToken:
        """Create new refresh token"""
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            revoked=False
        )
        
        self.session.add(refresh_token)
        await self.session.commit()
        await self.session.refresh(refresh_token)
        
        return refresh_token
    
    async def get_by_user_id(self, user_id: int) -> List[RefreshToken]:
        """Get all tokens for user"""
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.user_id == user_id)
        )
        return list(result.scalars().all())
    
    async def get_by_token(self, token: str) -> Optional[RefreshToken]:
        """Get token by value"""
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )
        return result.scalar_one_or_none()
    
    async def get_active_tokens(self) -> List[RefreshToken]:
        """Get active tokens (not revoked and not expired)"""
        now = datetime.utcnow()
        result = await self.session.execute(
            select(RefreshToken).where(
                RefreshToken.revoked == False,
                RefreshToken.expires_at > now
            )
        )
        return list(result.scalars().all())
    
    async def revoke_token(self, token: str) -> bool:
        """Mark token as revoked"""
        refresh_token = await self.get_by_token(token)
        if not refresh_token:
            return False
        
        refresh_token.revoked = True
        await self.session.commit()
        
        return True
    
    async def delete_expired_tokens(self) -> int:
        """Delete expired tokens, return count"""
        now = datetime.utcnow()
        result = await self.session.execute(
            delete(RefreshToken).where(RefreshToken.expires_at < now)
        )
        await self.session.commit()
        
        return result.rowcount