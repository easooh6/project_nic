from uuid import uuid4
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

    async def create_refresh(self, user_id: int) -> str:

        raw_token = uuid4().hex
        hashed = self._hash.hash(raw_token)

        expires_at = datetime.now(timezone.utc) + timedelta(
            days=self._config.REFRESH_TOKEN_EXPIRE_DAYS
        )

        await self._repo.create_token(
            token=hashed,
            user_id=user_id,
            expires_at=expires_at,
        )

        return raw_token
