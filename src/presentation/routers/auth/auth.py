from fastapi import APIRouter, status, Depends, HTTPException
from src.domain.exceptions.auth.auth import EmailAlreadyExistsException, InvalidResetTokenException, ResetTokenNotFoundException
from src.domain.exceptions.user.user import UserNotExistsException
from src.presentation.di.service.auth.verify import get_verify_access
from src.presentation.routers.auth.responses.me import MeResponse
from src.domain.dto.auth.token import TokenDTO
from src.domain.user.user import UserService
from src.domain.dto.user.user_dto import UserRead, UserLogin
from src.domain.auth.auth_service import AuthService
from src.domain.auth.password_reset_service import PasswordResetService
from src.presentation.routers.auth.responses.refresh import RefreshResponse
from src.presentation.routers.auth.requests.refresh import RefreshRequest
from src.presentation.routers.auth.requests.user_register import UserRegisterRequest
from src.presentation.routers.auth.responses.user_register import UserRegisterResponse
from src.presentation.requests import ForgotPasswordRequest, ResetPasswordRequest
from src.presentation.responses import ForgotPasswordResponse, ResetPasswordResponse
from src.logger.logger import setup_logging

logger = setup_logging("auth_router")

router = APIRouter()

@router.get('/me', response_model=MeResponse, status_code=status.HTTP_200_OK)
async def me(user: TokenDTO = Depends(get_verify_access)):
    service = UserService()
    dto = await service.get_user_by_id(user.sub)
    response = MeResponse(**dto.model_dump())

    return response

@router.post('/refresh', response_model=RefreshResponse, status_code=status.HTTP_200_OK)
async def refresh(refresh_request: RefreshRequest):

    service = AuthService()
    access = await service.renew_access(refresh_request.refresh)
    response = RefreshResponse(access=access)

    return response

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_register: UserRegisterRequest): # тут получаем данные для серва suth_service
    """регистрация"""
    try:
        auth_service = AuthService()
        user = await auth_service.register_user(user_register) # а точнее .register_user передает

        return UserRegisterResponse( #Возвращаем на ручку только то что можно видеть пользователю
            id=user.id,
            email=user.email,
            role=user.role,
            created_at=user.created_at
        )
    except EmailAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {e}"
        )
    
@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(payload: UserLogin):
    """логин с JWT токеном"""
    try:
        auth_service = AuthService()
        result = await auth_service.login_user(payload.email, payload.password)
        logger.info(f"User logged in: {payload.email}")
        return result
    except ValueError as e:
        logger.warning(f"Failed login attempt for email: {payload.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Login error for {payload.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {e}"
        )


@router.post("/forgot", response_model=ForgotPasswordResponse, status_code=status.HTTP_200_OK)
async def forgot_password(request: ForgotPasswordRequest):
    """Запрос на восстановление пароля"""
    try:
        service = PasswordResetService()
        reset_token = await service.create_reset_token(request.email)
        
        # TODO: Отправить токен на email (интеграция с email-сервисом)
        # В реальном приложении токен отправляется на email
        # Здесь для демонстрации возвращаем в ответе
        
        logger.info(f"Password reset requested for: {request.email}")
        return ForgotPasswordResponse(
            message="Password reset token has been sent to your email",
            email=request.email
        )
    except UserNotExistsException:
        # Из соображений безопасности не раскрываем существование email
        logger.warning(f"Password reset requested for non-existent email: {request.email}")
        return ForgotPasswordResponse(
            message="If this email exists, password reset instructions have been sent",
            email=request.email
        )
    except Exception as e:
        logger.error(f"Forgot password error for {request.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process password reset request"
        )


@router.post("/reset", response_model=ResetPasswordResponse, status_code=status.HTTP_200_OK)
async def reset_password(request: ResetPasswordRequest):
    """Сброс пароля с использованием токена"""
    try:
        service = PasswordResetService()
        await service.reset_password(request.token, request.new_password)
        
        logger.info(f"Password successfully reset using token")
        return ResetPasswordResponse(
            message="Password has been successfully reset"
        )
    except ResetTokenNotFoundException:
        logger.warning(f"Invalid or expired reset token used")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    except UserNotExistsException:
        logger.error(f"User not found during password reset")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password"
        )
