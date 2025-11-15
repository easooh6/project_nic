from src.domain.auth.verify_user import UserVerify
from src.infrastructure.db.repositories.user import UserRepository
from fastapi import Depends

async def get_user_verify(repo: UserRepository = Depends()
        ,jwt: JWTManager = Depends()):
    
    return UserVerify(repo,jwt)
