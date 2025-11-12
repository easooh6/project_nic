from passlib.context import CryptContext
from src.infrastructure.db.repositories.user import UserRepository
from src.domain.entities.user import UserCreate, UserRead
from src.domain.enums.role import RoleEnum  # если роли есть

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """регистрация"""

    def __init__(self):
        self.user_repo = UserRepository()

    async def register_user(self, data: UserCreate) -> UserRead | None:
        
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise ValueError("Email already exists")

       
        password_hash = pwd_context.hash(data.password)

        
        user = await self.user_repo.create_user(
            email=data.email,
            password_hash=password_hash,
            role=RoleEnum.USER
        )

        return UserRead.model_validate(user)