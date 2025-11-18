from fastapi import APIRouter, HTTPException, status
from src.domain.dto.user import UserRegister, UserRead, UserLogin
from src.domain.services.auth_service import AuthService

router = APIRouter()


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