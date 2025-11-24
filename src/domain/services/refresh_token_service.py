from uuid import uuid4
from datetime import datetime, timedelta, timezone

from src.infrastructure.settings.settings import settings
from src.infrastructure.db.repositories.token import RefreshTokenRepository
from src.domain.services.hash_service import HashService


class RefreshTokenService:
    def __init__(self) -> None:
        self._repo = RefreshTokenRepository()
        self._hash = HashService()

    async def create_refresh_token(self, user_id: int) -> str:

        raw_token = uuid4().hex

        hashed = self._hash.hash(raw_token)

        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.auth.REFRESH_TOKEN_EXPIRE_DAYS
        )

        await self._repo.create_token(
            token=hashed,
            user_id=user_id,
            expires_at=expires_at
        )

        return raw_token
