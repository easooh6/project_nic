from src.infrastructure.db.repositories.user import UserRepository
from src.domain.dto.user import UserRegister, UserRead, LoginResponse
from src.infrastructure.utils.password import hash_password, verify_password
from src.domain.auth.jwt_service import JWT

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.jwt_service = JWT()

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
        
        return LoginResponse(
            access_token=access_token,
            refresh_token="",  # Пока пустая строка
            token_type="bearer",
            user=UserRead.model_validate(user)
        )
