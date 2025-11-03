from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from src.infrastructure.db.models.refresh_token import RefreshToken

class IRefreshTokenRepository(ABC):
    
    @abstractmethod
    async def create_token(self, token: str, user_id: int, expires_at: datetime) -> RefreshToken:
        """Create new refresh token"""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[RefreshToken]:
        """Get all tokens for user"""
        pass
    
    @abstractmethod
    async def get_by_token(self, token: str) -> Optional[RefreshToken]:
        """Get token by value"""
        pass
    
    @abstractmethod
    async def get_active_tokens(self) -> List[RefreshToken]:
        """Get active tokens (not revoked and not expired)"""
        pass
    
    @abstractmethod
    async def revoke_token(self, token: str) -> bool:
        """Mark token as revoked"""
        pass
    
    @abstractmethod
    async def delete_expired_tokens(self) -> int:
        """Delete expired tokens, return count"""
        pass