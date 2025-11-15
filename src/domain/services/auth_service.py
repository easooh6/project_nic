from src.domain.entities.user import UserRegister, UserLogin, UserResponse, LoginResponse
from src.domain.enums.role import RoleEnum
from src.infrastructure.db.repositories.user import UserRepository
from src.infrastructure.utils.password import hash_password, verify_password


class AuthService:
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    async def register_user(self, user_data: UserRegister) -> UserResponse:
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        hashed_password = hash_password(user_data.password)
        
        user = await self.user_repo.create_user(
            email=user_data.email,
            password_hash=hashed_password,
            role=user_data.role
        )
        
        return UserResponse.model_validate(user)
    
    async def login_user(self, user_data: UserLogin) -> LoginResponse:
        user = await self.user_repo.get_by_email(user_data.email)
        if not user:
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User account is disabled")
        
        if not verify_password(user_data.password, user.password_hash):
            raise ValueError("Invalid email or password")
        
        # TODO: Заменить на реальный JWT когда jwt_service будет готов
        return LoginResponse(
            access="todo", 
            user=UserResponse.model_validate(user)
        )
    
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        return UserResponse.model_validate(user)