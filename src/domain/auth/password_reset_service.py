import secrets
from src.infrastructure.db.repositories.user import UserRepository
from src.infrastructure.redis.repository import RedisRepository
from src.domain.services.hash_service import HashService
from src.domain.services.email_service import EmailService
from src.domain.exceptions.user.user import UserNotExistsException
from src.domain.exceptions.auth.auth import InvalidResetTokenException, ResetTokenNotFoundException
from src.domain.templates.password_reset_email import get_password_reset_email_template
from src.logger.logger import setup_logging

logger = setup_logging("app")

class PasswordResetService:
    
    RESET_TOKEN_EXPIRY = 3600  
    RESET_TOKEN_PREFIX = "password_reset:"
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.email_service = EmailService()
        self.redis_repo = RedisRepository()
        self.hash_service = HashService()
    
    async def create_reset_token(self, email: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if not user:
            logger.warning(f"Password reset attempt for non-existent email: {email}")
            raise UserNotExistsException()
        
        reset_token = secrets.token_urlsafe(32)
        
        token_hash = self.hash_service.hash_token(reset_token)
        redis_key = f"{self.RESET_TOKEN_PREFIX}{token_hash}"
        await self.redis_repo.set(
            redis_key,
            str(user.id),
            ttl=self.RESET_TOKEN_EXPIRY
        )

        subject, body = get_password_reset_email_template(reset_token)
        
        await self.email_service.send_email(email, subject, body)
        logger.info(f"Password reset email sent to {email}")
        
        logger.info(f"Password reset token created for user_id={user.id}, email={email}")
        return reset_token
    
    async def validate_reset_token(self, token: str) -> bool:
        token_hash = self.hash_service.hash_token(token)
        redis_key = f"{self.RESET_TOKEN_PREFIX}{token_hash}"
        
        exists = await self.redis_repo.exists(redis_key)
        if not exists:
            logger.warning(f"Token validation failed: token not found or expired")
            raise ResetTokenNotFoundException()
        
        logger.info(f"Token validated successfully")
        return True
    
    async def reset_password(self, token: str, new_password: str) -> None:
        token_hash = self.hash_service.hash_token(token)
        redis_key = f"{self.RESET_TOKEN_PREFIX}{token_hash}"
        
        user_id_str = await self.redis_repo.get(redis_key)
        if not user_id_str:
            logger.warning(f"Invalid or expired reset token used")
            raise ResetTokenNotFoundException()
        
        user_id = int(user_id_str)
        
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            logger.error(f"User not found for reset token, user_id={user_id}")
            raise UserNotExistsException()

        password_hash = self.hash_service.hash(new_password)
        await self.user_repo.update_user(user_id, {"password_hash": password_hash})
        
        await self.redis_repo.delete(redis_key)
        
        logger.info(f"Password successfully reset for user_id={user_id}, email={user.email}")
