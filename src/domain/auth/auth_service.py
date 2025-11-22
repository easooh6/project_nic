from uuid import uuid4
from datetime import datetime, timedelta, timezone

from src.infrastructure.settings.settings import settings

from src.infrastructure.db.repositories.user import UserRepository
from src.infrastructure.db.repositories.token import RefreshTokenRepository
from src.domain.dto.user.user_dto import UserRead, LoginResponse #потом убрать userRead
from src.domain.auth.jwt_service import JWT, RefreshValidator
from src.domain.entities.refresh import RefreshEntity
from src.domain.entities.user import User
from src.domain.exceptions.user.user import UserNotExistsException
from src.domain.exceptions.auth.auth import EmailAlreadyExistsException, RefreshNotFoundException
from src.infrastructure.utils.password import hash_password, verify_password
from src.presentation.routers.auth.requests.user_register import UserRegisterRequest

class AuthService:
    """регистрация"""

    def __init__(self):
        self.user_repo = UserRepository()
        self.refresh_repo = RefreshTokenRepository()
        self.access_service = JWT()
    
    async def _create_refresh_token(self, user_id: int) -> str:
        token = uuid4().hex

        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.auth.REFRESH_TOKEN_EXPIRE_DAYS
        )

        await self.refresh_repo.create_token(
            token= token,          #token
            user_id=user_id,
            expires_at=expires_at
        )

        return token


    async def register_user(self, data: UserRegisterRequest):
        
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise EmailAlreadyExistsException()

       
        password_hash = hash_password(data.password)

        
        user = await self.user_repo.create_user(
            email=data.email,
            password_hash=password_hash,
            role=data.role
        )

        return user #просто возвращаем ORM-модель т.к. UserRead должен быть удален
    
    async def login_user(self, email: str, password: str) -> LoginResponse:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User account is disabled")
        
        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")
        
        access_token = self.access_service.create_access_token(user.id, user.role)

        refresh_token = await self._create_refresh_token(user.id)

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserRead.model_validate(user)
        )

        
    async def renew_access(self, refresh_token: str) -> str:

        token = await self.refresh_repo.get_by_token(refresh_token)
        
        if token is None:
            raise RefreshNotFoundException
        
        entity_refresh = RefreshEntity.model_validate(token)

        RefreshValidator.validate(entity_refresh)
        
        user_id = entity_refresh.user_id
        user = await self.user_repo.get_by_id(user_id)

        if user is None:
            raise UserNotExistsException

        entity_user = User.model_validate(user)
        
        access = self.access_service.create_access_token(user_id, entity_user.role)

        return access