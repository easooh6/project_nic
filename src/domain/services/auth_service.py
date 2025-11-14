from passlib.context import CryptContext
from src.infrastructure.db.repositories.user import UserRepository
from domain.dto.user import UserRegister, UserRead
from src.infrastructure.utils.password import HashingService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """регистрация"""

    def __init__(self):
        self.user_repo = UserRepository()

    async def register_user(self, data: UserRegister) -> UserRead | None:
        
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise ValueError("Email already exists")

       
        password_hash = HashingService.hash_password(data.password)

        
        user = await self.user_repo.create_user(
            email=data.email,
            password_hash=password_hash,
            role=data.role
        )

        return UserRead.model_validate(user)