from abc import ABC, abstractmethod
from src.infrastructure.db.models.file_upload import FileUpload


class IFileUploadRepository(ABC):

    # CREATE 
    @abstractmethod
    async def create(self, path: str, size_bytes: int, mime: str, owner_user_id: int) -> FileUpload:
        pass

    # READ  по id
    @abstractmethod
    async def get_by_id(self, file_id: int) -> FileUpload | None:
        pass

    # READ всего по owner_user_id
    @abstractmethod
    async def get_by_owner(self, owner_user_id: int) -> list[FileUpload]:
        pass

    # UPDATE путь | размер
    @abstractmethod
    async def update(self, file_id: int, path: str | None = None, size_bytes: int | None = None) -> FileUpload | None:
        pass

    # DELETE 
    @abstractmethod
    async def delete(self, file_id: int) -> bool:
        pass
