from src.domain.enums.role import RoleEnum
from src.infrastructure.db.repositories.user import UserRepository
from src.domain.exceptions.user.user import RoleException
from src.domain.exceptions.user.user import UserNotExistsException, UserStateException
from src.domain.dto.auth.token import TokenDTO
from src.domain.auth.jwt_service import JWT

class UserVerify:

    def __init__(self, user: UserRepository, jwt: JWT):
        self.user = user
        self.jwt = jwt

    def _check_role(self, role: str):

        if role != RoleEnum.admin:
            raise RoleException
    
    async def _check_existence_and_state(self, user_id):
        
        user = await self.user.get_by_id(user_id)

        if user is None:
            raise UserNotExistsException

        if not user.is_active:
            raise UserStateException

    async def verify_admin(self, token: str) -> TokenDTO:

        dto = await self.verify_access(token)
        role = dto.role
        self._check_role(role)

        return dto

    async def verify_access(self, token: str) -> TokenDTO:

        payload = self.jwt.decode_access_token(token)
        
        user_id = payload.get("sub")
        await self._check_existence_and_state(user_id)
        
        dto = TokenDTO.model_validate(payload)

        return dto
