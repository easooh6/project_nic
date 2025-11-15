from fastapi import APIRouter, HTTPException, status
from src.domain.dto.user import UserRegister, UserRead
from src.domain.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserRegister):
    """регистрация"""
    try:
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