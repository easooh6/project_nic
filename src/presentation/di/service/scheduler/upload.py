from src.domain.upload.file_upload import FileUploadService

async def get_file_upload_service() -> FileUploadService:
    return FileUploadService()