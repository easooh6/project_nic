import secrets
from src.infrastructure.db.repositories.user import UserRepository
from src.infrastructure.redis.client import get_redis_client
from src.infrastructure.utils.password import hash_password
from src.domain.exceptions.user.user import UserNotExistsException
from src.domain.exceptions.auth.auth import InvalidResetTokenException, ResetTokenNotFoundException
from src.logger.logger import setup_logging

logger = setup_logging("password_reset")

class PasswordResetService:
    """Сервис для восстановления пароля"""
    
    RESET_TOKEN_EXPIRY = 3600  # 1 час в секундах
    RESET_TOKEN_PREFIX = "password_reset:"
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    async def create_reset_token(self, email: str) -> str:
        """Создает токен для сброса пароля"""
        # Проверяем существование пользователя
        user = await self.user_repo.get_by_email(email)
        if not user:
            logger.warning(f"Password reset attempt for non-existent email: {email}")
            raise UserNotExistsException()
        
        # Генерируем случайный токен
        reset_token = secrets.token_urlsafe(32)
        
        # Сохраняем в Redis
        redis_client = await get_redis_client()
        redis_key = f"{self.RESET_TOKEN_PREFIX}{reset_token}"
        await redis_client.setex(
            redis_key,
            self.RESET_TOKEN_EXPIRY,
            str(user.id)
        )
        
        logger.info(f"Password reset token created for user_id={user.id}, email={email}")
        return reset_token
    
    async def reset_password(self, token: str, new_password: str) -> None:
        """Сбрасывает пароль используя токен"""
        redis_client = await get_redis_client()
        redis_key = f"{self.RESET_TOKEN_PREFIX}{token}"
        
        # Получаем user_id из Redis
        user_id_str = await redis_client.get(redis_key)
        if not user_id_str:
            logger.warning(f"Invalid or expired reset token used")
            raise ResetTokenNotFoundException()
        
        user_id = int(user_id_str)
        
        # Проверяем существование пользователя
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            logger.error(f"User not found for reset token, user_id={user_id}")
            raise UserNotExistsException()
        
        # Обновляем пароль
        password_hash = hash_password(new_password)
        await self.user_repo.update_user(user_id, {"password_hash": password_hash})
        
        # Удаляем использованный токен
        await redis_client.delete(redis_key)
        
        logger.info(f"Password successfully reset for user_id={user_id}, email={user.email}")
