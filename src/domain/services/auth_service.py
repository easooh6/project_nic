from src.infrastructure.db.repositories.user import UserRepository
from src.domain.auth.requests import RegisterRequest
from src.domain.auth.responses import UserResponse, LoginResponse
from src.infrastructure.utils.password import hash_password, verify_password
from src.domain.jwt_service import JWT
from src.domain.exceptions import (
    UserNotExistsException, 
    UserStateException, 
    InvalidCredentialsException,
    EmailAlreadyExistsException
)

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.jwt_service = JWT()

    async def register_user(self, data: RegisterRequest) -> UserResponse:
        
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise EmailAlreadyExistsException()

        password_hash = hash_password(data.password)

        user = await self.user_repo.create_user(
            email=data.email,
            password_hash=password_hash,
            role=data.role
        )

        return UserResponse.model_validate(user)

    async def login_user(self, email: str, password: str) -> LoginResponse:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise InvalidCredentialsException()

        if not user.is_active:
            raise UserStateException()
        
        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsException()
        
        access_token = self.jwt_service.create_access_token(user.id, user.role)
        refresh_token = self.jwt_service.create_refresh_token(user.id)
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            user=UserResponse.model_validate(user)
        )

    async def renew_access(self, refresh_token: str) -> str:
        try:
            payload = self.jwt_service.decode_refresh_token(refresh_token)
            user_id = int(payload["sub"])
            await self._check_existence_and_state(user_id)
            user = await self.user_repo.get_by_id(user_id)
            
            new_access_token = self.jwt_service.create_access_token(user.id, user.role)
            return new_access_token
            
        except Exception:
            raise InvalidTokenException()

    async def _check_existence_and_state(self, user_id: int):
        user = await self.user_repo.get_by_id(user_id)

        if user is None:
            raise UserNotExistsException()

        if not user.is_active:
            raise UserStateException()
