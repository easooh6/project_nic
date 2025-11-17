from fastapi import APIRouter, status, Depends, HTTPException
from src.presentation.di.service.auth.verify import get_verify_access
from src.presentation.routers.auth.responses.me_response import MeResponse
from src.domain.dto.auth.token import TokenDTO
from src.domain.user.user import UserService
from src.domain.dto.user.user_dto import UserRegister, UserRead
from src.domain.auth.auth_service import AuthService

router = APIRouter()

@router.get('/me', response_model=MeResponse, status_code=status.HTTP_200_OK)
async def me(user: TokenDTO = Depends(get_verify_access)):
    service = UserService()
    dto = await service.get_user_by_id(user.sub)
    response = MeResponse(**dto.model_dump())

    return response

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserRegister):
    """регистрация"""
    try:
        auth_service = AuthService() # тоесть как понял, каждый запрос создаёт свой экземпляр AuthService 
        user = await auth_service.register_user(payload)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {e}"
        )