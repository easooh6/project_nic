from fastapi import APIRouter, status, Depends
from src.presentation.di.service.auth.verify import get_verify_access
from src.presentation.routers.auth.responses.me_response import MeResponse
from src.domain.dto.auth.token import TokenDTO
from src.domain.user.user import UserService

router = APIRouter()

@router.get('/me', response_model=MeResponse, status_code=status.HTTP_200_OK)
async def me(user: TokenDTO = Depends(get_verify_access)):
    service = UserService()
    dto = await service.get_user_by_id(user.sub)
    response = MeResponse(**dto.model_dump())

    return response
    