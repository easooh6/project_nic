from src.domain.enums.role import RoleEnum
from src.infrastructure.db.repositories.user import UserRepository
from src.domain.exceptions.auth.auth import RoleException
from src.domain.exceptions.user.user import UserNotExistsException
from src.domain.dto.auth.token import TokenDTO
from src.domain.auth.jwt_service import JWT

class UserVerify:

    def __init__(self, user: UserRepository, jwt: JWT):
        self.user = user
        self.jwt = jwt

    def _check_role(self, role: str):

        if role != RoleEnum.admin:
            raise RoleException
    
    def _check_existence(self, user_id):

        if self.user.get_by_id(user_id) is None:
            raise UserNotExistsException

    async def verify_admin(self, token: str) -> TokenDTO:

        dto = await self.verify_access(token)

        role = dto.role
        user_id = dto.sub

        self._check_role(role)
        self._check_existence(user_id)

        return dto

    async def verify_access(self, token: str) -> TokenDTO:

        payload = await self.jwt.decode_access_token(token)

        dto = TokenDTO.model_validate(payload)

        return dto
