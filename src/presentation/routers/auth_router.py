from fastapi import APIRouter, status
from src.domain.entities.user import UserCreate, UserRead
from src.domain.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserCreate):
    """регистрация"""
    user = await auth_service.register_user(payload)
    return user
    