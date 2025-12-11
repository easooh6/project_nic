from src.infrastructure.db.repositories.resource import ResourceRepository
from src.infrastructure.db.repositories.file_upload import FileUploadRepository
from src.infrastructure.settings.settings import settings
import asyncio
from src.logger.logger import setup_logging

logger = setup_logging("app")

class FileUploadService:

    def __init__(self):
        self.repo_resource = ResourceRepository()
        self.repo_upload = FileUploadRepository()
        self.settings = settings.upload

    def _blocking_recursive_search(self) -> set[str]:
        found_paths = set()
        root = self.settings.UPLOAD_ROOT

        for item_path in root.rglob('*'):
            if item_path.is_file():
                relative_path = item_path.relative_to(root)
                found_paths.add(str(relative_path))

        return found_paths

    def _blocking_delete(self, relative_path: set[str]):

        root = self.settings.UPLOAD_ROOT
        deleted = set()

        for path in relative_path:
            full_path = root / path
            if full_path.is_file():
                try:
                    full_path.unlink()
                    logger.debug("Successfully deleted file %s", str(path))
                    deleted.add(path)
                except Exception as e:
                    logger.error("Failed to delete file %s: %s", str(path), e)

        return deleted

    async def get_all_project_file_paths(self) -> set[str]:

        return await asyncio.to_thread(self._blocking_recursive_search)

    async def delete_file_paths(self, relative_path: set[str]):

        return await asyncio.to_thread(self._blocking_delete, relative_path)

    async def cleanup_uploads(self):

        paths_from_db = await self.repo_resource.get_resources_with_path()

        paths_from_disk = await self.get_all_project_file_paths()

        not_existed = paths_from_disk-paths_from_db

        if not not_existed:
            logger.debug("Files were not found to be deleted")
            return

        deleted_path = await self.delete_file_paths(not_existed)

        result = await self.repo_upload.delete_by_files(deleted_path)

        return result
