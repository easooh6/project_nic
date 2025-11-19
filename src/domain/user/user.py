from src.domain.dto.user.user_dto import UserDTO
from src.infrastructure.db.repositories.user import UserRepository
from src.domain.exceptions.user.user import UserNotExistsException

class UserService:
    
    def __init__(self):
        self.repo = UserRepository()
    
    async def get_user_by_id(self, user_id: int):

        user_raw = await self.repo.get_by_id(user_id)

        if user_raw is None:
            raise UserNotExistsException
        
        dto = UserDTO.model_validate(user_raw)

        return dto

