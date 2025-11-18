from src.infrastructure.db.repositories.user import UserRepository
from src.domain.dto.user import UserRegister, UserRead
from src.infrastructure.utils.password import hash_password, verify_password

from src.infrastructure.settings.settings import settings
from src.domain.services.refresh_token_service import RefreshTokenService
from src.infrastructure.db.repositories.token import RefreshTokenRepository

class HashService:
    def hash(self, value: str) -> str:
        return hash_password(value)

    def verify(self, value: str, hashed: str) -> bool:
        return verify_password(value, hashed)


class AuthService:
    """регистрация"""

    def __init__(self):
        self.user_repo = UserRepository()
        self.refresh_tokens = RefreshTokenService(
            refresh_token_repo=RefreshTokenRepository(),
            hash_service=HashService(),
            config=settings.auth,   
        )

    async def register_user(self, data: UserRegister) -> UserRead | None:
        
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise ValueError("Email already exists")

       
        password_hash = hash_password(data.password)

        
        user = await self.user_repo.create_user(
            email=data.email,
            password_hash=password_hash,
            role=data.role
        )

        return UserRead.model_validate(user)