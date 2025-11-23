from src.domain.auth.verify_user import UserVerify
from src.infrastructure.db.repositories.user import UserRepository
from fastapi import Depends
from src.domain.auth.jwt_service import JWT

async def get_user_verify(repo: UserRepository = Depends()
        ,jwt: JWT = Depends()):
    
    return UserVerify(repo,jwt)
