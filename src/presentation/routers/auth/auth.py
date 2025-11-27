from fastapi import APIRouter, status, Depends, HTTPException, Cookie, Response
from src.domain.exceptions.auth.auth import EmailAlreadyExistsException
from src.presentation.di.service.auth.verify import get_verify_access
from src.presentation.routers.auth.responses.me import MeResponse
from src.domain.dto.auth.token import TokenDTO
from src.domain.user.user import UserService
from src.domain.dto.user.user_dto import UserRead, UserLogin
from src.domain.auth.auth_service import AuthService
from src.presentation.routers.auth.responses.refresh import RefreshResponse
from src.presentation.routers.auth.requests.refresh import RefreshRequest
from src.presentation.routers.auth.requests.user_register import UserRegisterRequest
from src.presentation.routers.auth.responses.user_register import UserRegisterResponse
from src.presentation.routers.auth.responses.logout import LogoutResponse

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

