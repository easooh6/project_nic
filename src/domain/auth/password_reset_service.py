import secrets
from src.infrastructure.db.repositories.user import UserRepository
from src.infrastructure.redis.client import get_redis_client
from src.infrastructure.utils.hashing.password import hash_password
from src.domain.services.email_service import EmailService
from src.domain.exceptions.user.user import UserNotExistsException
from src.domain.exceptions.auth.auth import InvalidResetTokenException, ResetTokenNotFoundException
from src.logger.logger import setup_logging

logger = setup_logging("password_reset")

class PasswordResetService:
    
    RESET_TOKEN_EXPIRY = 3600  
    RESET_TOKEN_PREFIX = "password_reset:"
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.email_service = EmailService()
    
    async def create_reset_token(self, email: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if not user:
            logger.warning(f"Password reset attempt for non-existent email: {email}")
            raise UserNotExistsException()
        
        reset_token = secrets.token_urlsafe(32)
        
        redis_client = await get_redis_client()
        redis_key = f"{self.RESET_TOKEN_PREFIX}{reset_token}"
        await redis_client.setex(
            redis_key,
            self.RESET_TOKEN_EXPIRY,
            str(user.id)
        )

        subject = "Password Reset Request"
        body = f"""
Hello,

You requested a password reset. Please use the following token to reset your password:

Token: {reset_token}

This token will expire in 1 hour.

If you did not request this, please ignore this email.

Best regards,
Your Application Team
        """
        
        try:
            await self.email_service.send_email(email, subject, body)
            logger.info(f"Password reset email sent to {email}")
        except Exception as e:
            logger.error(f"Failed to send password reset email to {email}: {e}")
        
        logger.info(f"Password reset token created for user_id={user.id}, email={email}")
        return reset_token
    
    async def reset_password(self, token: str, new_password: str) -> None:
        redis_client = await get_redis_client()
        redis_key = f"{self.RESET_TOKEN_PREFIX}{token}"
        
        user_id_str = await redis_client.get(redis_key)
        if not user_id_str:
            logger.warning(f"Invalid or expired reset token used")
            raise ResetTokenNotFoundException()
        
        user_id = int(user_id_str)
        
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            logger.error(f"User not found for reset token, user_id={user_id}")
            raise UserNotExistsException()
        
        from src.infrastructure.utils.hashing.password import hash_password
        password_hash = hash_password(new_password)
        await self.user_repo.update_user(user_id, {"password_hash": password_hash})
        
        await redis_client.delete(redis_key)
        
        logger.info(f"Password successfully reset for user_id={user_id}, email={user.email}")
