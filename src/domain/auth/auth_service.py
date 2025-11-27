from src.infrastructure.db.repositories.user import UserRepository
from src.infrastructure.db.repositories.token import RefreshTokenRepository
from src.domain.dto.user.user_dto import UserRead, LoginResponse
from src.domain.auth.jwt_service import JWT, RefreshValidator
from src.domain.entities.refresh import RefreshEntity
from src.domain.entities.user import User
from src.domain.exceptions.user.user import UserNotExistsException
from src.domain.exceptions.auth.auth import EmailAlreadyExistsException, RefreshNotFoundException
from src.presentation.routers.auth.requests.user_register import UserRegisterRequest
from src.domain.exceptions.auth.auth import RefreshNotFoundException
from src.domain.services.refresh_token_service import RefreshTokenService
from src.domain.services.hash_service import HashService
from src.logger.logger import setup_logging

logger = setup_logging("app")

class AuthService:
    """регистрация"""

    def __init__(self):
        self.user_repo = UserRepository()
        self.refresh_repo = RefreshTokenRepository()
        self.access_service = JWT()
        self.refresh_service = RefreshTokenService()   # <-- добавили как лидер сказал
        self.hash = HashService()

    async def register_user(self, data: UserRegisterRequest):
        
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise EmailAlreadyExistsException()

        password_hash = self.hash.hash(data.password)

        user = await self.user_repo.create_user(
            email=data.email,
            password_hash=password_hash,
            role=data.role
        )

        logger.debug("User %s registered", str(user.id))
        return user
    
    async def login_user(self, email: str, password: str) -> LoginResponse:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User account is disabled")
        
        if not self.hash.verify(password, user.password_hash):
            raise ValueError("Invalid email or password")
        
        access_token = self.access_service.create_access_token(user.id, user.role)

        # <-- Теперь создаём refresh-токен через RefreshTokenService
        refresh_token = await self.refresh_service.create_refresh_token(user.id)

        logger.debug("User %s logged in", str(user.id))
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserRead.model_validate(user)
        )

    async def renew_access(self, refresh_token: str) -> str:

        hashed_token = self.hash.hash_token(refresh_token)
        token = await self.refresh_repo.get_by_token(hashed_token)
        
        if token is None:
            raise RefreshNotFoundException()

        entity_refresh = RefreshEntity.model_validate(token)

        RefreshValidator.validate(entity_refresh)
        
        user_id = entity_refresh.user_id
        user = await self.user_repo.get_by_id(user_id)

        if user is None:
            raise UserNotExistsException()

        entity_user = User.model_validate(user)
        
        access = self.access_service.create_access_token(user_id, entity_user.role)
        
        logger.debug("User %s got new access", str(user.id))
        return access

    async def logout(self, token: str) -> bool: 
        
        hashed_token = self.hash.hash_token(token)

        revoked_token = await self.refresh_repo.revoke_token(hashed_token)

        if not revoked_token:
            raise RefreshNotFoundException()

        logger.debug("User with token %s**** logged out", str(hashed_token)[:5])
        return True