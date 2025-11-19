from src.infrastructure.db.repositories.user import UserRepository
from src.infrastructure.db.repositories.token import RefreshTokenRepository
from src.domain.dto.user import UserRegister, UserRead
from src.infrastructure.utils.password import hash_password, verify_password
from src.domain.jwt_service import JWT
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel

class LoginResponse(BaseModel):
    """Модель ответа для логина с JWT токенами"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserRead

    class Config:
        from_attributes = True

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.jwt_service = JWT()
        self.refresh_token_repo = RefreshTokenRepository()

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

    async def login_user(self, email: str, password: str) -> LoginResponse:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User account is disabled")
        
        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")
        
    
        access_token = self.jwt_service.create_access_token(user.id, user.role)
        refresh_token = self.jwt_service.create_refresh_token(user.id)
        
        # Сохраняем refresh токен в БД
        expires_at = datetime.now(timezone.utc) + timedelta(days=self.jwt_service.refresh_expire_days)
        await self.refresh_token_repo.create_token(
            token=refresh_token,
            user_id=user.id,
            expires_at=expires_at
        )
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserRead.model_validate(user)
        )
