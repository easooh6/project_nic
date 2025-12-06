from src.tasks.broker import broker
from taskiq import TaskiqDepends
from src.presentation.di.service.scheduler.upload import get_file_upload_service
from src.domain.upload.file_upload import FileUploadService
from src.logger.logger import setup_logging

logger = setup_logging("app")

@broker.task
async def upload_task(service: FileUploadService = TaskiqDepends(get_file_upload_service)):
    logger.info("Starting cleanup-uploads")

    deleted_count = await service.cleanup_uploads()

    logger.info("Deleted cleanup-uploads %d", deleted_count)

    return deleted_count