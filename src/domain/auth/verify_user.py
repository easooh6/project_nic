from src.domain.enums.role import RoleEnum
from src.infrastructure.db.repositories.user import UserRepository
<<<<<<< HEAD
from src.domain.exceptions.auth.auth import RoleException
from src.domain.exceptions.user.user import UserNotExistsException
from src.domain.dto.auth.token import TokenDTO

class UserVerify:

    def __init__(self, user: UserRepository, jwt: JWTManager):
=======
from src.domain.exceptions.user.user import RoleException
from src.domain.exceptions.user.user import UserNotExistsException, UserStateException
from src.domain.dto.auth.token import TokenDTO
from src.domain.auth.jwt_service import JWT

class UserVerify:

    def __init__(self, user: UserRepository, jwt: JWT):
>>>>>>> 8e88b8e6dba6e6c36e2d9bca05367e3ccf7dfe7c
        self.user = user
        self.jwt = jwt

    def _check_role(self, role: str):

        if role != RoleEnum.admin:
            raise RoleException
    
<<<<<<< HEAD
    def _check_existence(self, user_id):

        if self.user.get_by_id(user_id) is None:
            raise UserNotExistsException

    async def verify_admin(self, token: str) -> TokenDTO:

        dto = await self.verify_access(token)

        role = dto.role
        user_id = dto.sub

        self._check_role(role)
        self._check_existence(user_id)
=======
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
>>>>>>> 8e88b8e6dba6e6c36e2d9bca05367e3ccf7dfe7c

        return dto

    async def verify_access(self, token: str) -> TokenDTO:

<<<<<<< HEAD
        payload = await self.jwt.decode_access_token(token)

=======
        payload = self.jwt.decode_access_token(token)
        
        user_id = payload.get("sub")
        await self._check_existence_and_state(user_id)
        
>>>>>>> 8e88b8e6dba6e6c36e2d9bca05367e3ccf7dfe7c
        dto = TokenDTO.model_validate(payload)

        return dto
