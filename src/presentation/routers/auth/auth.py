from fastapi import APIRouter, status, Depends, HTTPException, Cookie, Response
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
from src.presentation.routers.auth.responses.logout import LogoutResponse
from src.presentation.requests import ForgotPasswordRequest, ResetPasswordRequest
from src.presentation.responses import ForgotPasswordResponse, ResetPasswordResponse
from src.logger.logger import setup_logging

logger = setup_logging("app")

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

@router.post("/logout", status_code=status.HTTP_200_OK, response_model=LogoutResponse)
async def logout(response: Response, refresh_token: str = Cookie(default=None)):
    auth_service = AuthService()
    if not refresh_token:
        return LogoutResponse(status=False, message="Server got None instead of Refresh Token")
    
    await auth_service.logout(refresh_token)

    response.delete_cookie("refresh_token")

    return LogoutResponse()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_register: UserRegisterRequest): 
    try:
        auth_service = AuthService()
        user = await auth_service.register_user(user_register) 

        return UserRegisterResponse( 
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
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {e}"
        )


@router.post("/forgot", response_model=ForgotPasswordResponse, status_code=status.HTTP_200_OK)
async def forgot_password(request: ForgotPasswordRequest):
    service = PasswordResetService()
    await service.create_reset_token(request.email)
    logger.info(f"Password reset requested for: {request.email}")
    return ForgotPasswordResponse(
        message="Password reset token has been sent to your email",
        email=request.email
    )


@router.get("/reset-validate-token", status_code=status.HTTP_200_OK)
async def validate_reset_token(token: str):
    service = PasswordResetService()
    await service.validate_reset_token(token)
    logger.info(f"Reset token validated successfully")
    return {"valid": True, "message": "Token is valid"}


@router.post("/reset-password", response_model=ResetPasswordResponse, status_code=status.HTTP_200_OK)
async def reset_password(request: ResetPasswordRequest):
    service = PasswordResetService()
    await service.reset_password(request.token, request.new_password)
    logger.info(f"Password successfully reset")
    return ResetPasswordResponse(
        message="Password has been successfully reset"
    )
