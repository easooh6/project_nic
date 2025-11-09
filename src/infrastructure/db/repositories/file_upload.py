from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.db.models.file_upload import FileUpload
from src.infrastructure.db.db import get_db_session




class FileUploadRepository():

    def __init__(self):
        # создание сессии       
        self.session_factory = get_db_session
    # CREATE 
    async def create(self, path: str, size_bytes: int, mime: str, owner_user_id: int) -> FileUpload:
        try:
            async with self.session_factory() as session:
                new_file = FileUpload(
                path=path,
                size_bytes=size_bytes,
                mime=mime,
                owner_user_id=owner_user_id
            )
            session.add(new_file)
            await session.commit()
            await session.refresh(new_file)
            return new_file
        except Exception as e:
                await self.session.rollback()
                print(f"[ERROR][CREATE] {e}")
                # rollback возможен только если сессия открыта
                try:
                    await session.rollback()
                except Exception:
                    pass
                return None

    # READ  по id
    async def get_by_id(self, file_id: int) -> FileUpload | None:
        async with self.session_factory() as session:
            result = await session.execute(
                select(FileUpload).where(FileUpload.id == file_id)
            )
            return result.scalar_one_or_none()

    # READ всего по owner_user_id
    async def get_by_owner(self, owner_user_id: int) -> list[FileUpload]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(FileUpload).where(FileUpload.owner_user_id == owner_user_id)
            )
            return result.scalars().all()

    # UPDATE путь | размер
    async def update(self, file_id: int, path: str | None = None, size_bytes: int | None = None) -> FileUpload | None:
        try:
            async with self.session_factory() as session:
                result = await session.execute(
                    select(FileUpload).where(FileUpload.id == file_id)
                )
                file = result.scalar_one_or_none()
                if not file:
                    print(f"[WARN][UPDATE] File with id={file_id} not found")
                    return None

                if path is not None:
                    file.path = path
                if size_bytes is not None:
                    file.size_bytes = size_bytes

                await session.commit()
                await session.refresh(file)
                return file
        except Exception as e:
            print(f"[ERROR][UPDATE] {e}")
            try:
                await session.rollback()
            except Exception:
                pass
            return None

    # DELETE 
    async def delete(self, file_id: int) -> bool:
        try:
            async with self.session_factory() as session:
                result = await session.execute(
                    select(FileUpload).where(FileUpload.id == file_id)
                )
                file = result.scalar_one_or_none()
                if not file:
                    print(f"[WARN][DELETE] File with id={file_id} not found")
                    return False

                await session.delete(file)
                await session.commit()
                return True
        except Exception as e:
            print(f"[ERROR][DELETE] {e}")
            try:
                await session.rollback()
            except Exception:
                pass
            return False