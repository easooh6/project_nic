from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.db.models.file_upload import FileUpload


class FileUploadRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    # CREATE 
    async def create(self, path: str, size_bytes: int, mime: str, owner_user_id: int) -> FileUpload:
        new_file = FileUpload(
            path=path,
            size_bytes=size_bytes,
            mime=mime,
            owner_user_id=owner_user_id
        )
        self.session.add(new_file)
        await self.session.commit()
        await self.session.refresh(new_file)
        return new_file

    # READ  по id
    async def get_by_id(self, file_id: int) -> FileUpload | None:
        result = await self.session.execute(
            select(FileUpload).where(FileUpload.id == file_id)
        )
        return result.scalar_one_or_none()

    # READ всего по owner_user_id
    async def get_by_owner(self, owner_user_id: int) -> list[FileUpload]:
        result = await self.session.execute(
            select(FileUpload).where(FileUpload.owner_user_id == owner_user_id)
        )
        return result.scalars().all()

    # UPDATE путь | размер
    async def update(self, file_id: int, path: str | None = None, size_bytes: int | None = None) -> FileUpload | None:
        file = await self.get_by_id(file_id)
        if not file:
            return None

        if path is not None:
            file.path = path
        if size_bytes is not None:
            file.size_bytes = size_bytes

        await self.session.commit()
        await self.session.refresh(file)
        return file

    # DELETE 
    async def delete(self, file_id: int) -> bool:
        file = await self.get_by_id(file_id)
        if not file:
            return False

        await self.session.delete(file)
        await self.session.commit()
        return True
