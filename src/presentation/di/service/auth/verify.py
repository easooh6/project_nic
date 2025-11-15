from src.domain.auth.verify_user import UserVerify
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.presentation.di.service.auth.auth_service import get_user_verify

security = HTTPBearer()

async def get_verify_access(credentials: HTTPAuthorizationCredentials = Depends(security),
                            service: UserVerify = Depends(get_user_verify)):
    
    token = credentials.credentials
    dto = await service.verify_access(token)

    return dto

async def get_verify_admin(credentials: HTTPAuthorizationCredentials = Depends(security),
                           service: UserVerify = Depends(get_user_verify)):
    
    token = credentials.credentials
    dto = await service.verify_admin(token)

    return dto