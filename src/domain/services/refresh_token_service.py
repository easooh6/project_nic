from uuid import uuid4
from typing import Optional
from datetime import datetime, timedelta, timezone

from src.infrastructure.db.repositories.token import RefreshTokenRepository


class RefreshTokenService:
    def __init__(
        self,
        refresh_token_repo: RefreshTokenRepository,
        hash_service,   
        config,         
    ) -> None:
        self._repo = refresh_token_repo
        self._hash = hash_service
        self._config = config

    async def create_refresh_token(self, user_id: int) -> str:
        raw_token = uuid4().hex                     
        token_hash = self._hash.hash(raw_token)      

        expires_at = datetime.now(timezone.utc) + timedelta(
            days=self._config.REFRESH_TOKEN_EXPIRE_DAYS
        )

        await self._repo.create_token(
            token=token_hash,        
            user_id=user_id,
            expires_at=expires_at,
        )

        return raw_token

    async def decode_refresh_token(self, raw_token: str) -> dict:
        active_tokens = await self._repo.get_active_tokens()

        for token_model in active_tokens:
            if self._hash.verify(raw_token, token_model.token):
                return {
                    "sub": str(token_model.user_id),
                    "type": "refresh",
                    "exp": token_model.expires_at,
                }

        raise ValueError("Invalid or expired refresh token")

    
    async def validate_refresh_token(self, raw_token: str) -> Optional[int]: 

        active_tokens = await self._repo.get_active_tokens()

        for token_model in active_tokens:
            if self._hash.verify(raw_token, token_model.token):
                return token_model.user_id

        return None

    async def revoke_all_for_user(self, user_id: int) -> int:
        tokens = await self._repo.get_by_user_id(user_id)
        count = 0

        for token_model in tokens:
            if not token_model.revoked:
                ok = await self._repo.revoke_token(token_model.token)
                if ok:
                    count += 1

        return count
