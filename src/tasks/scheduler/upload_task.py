from src.tasks.broker import broker
from taskiq import TaskiqDepends
from src.presentation.di.service.scheduler.upload import get_file_upload_service
from src.domain.upload.file_upload import FileUploadService
from src.logger.logger import setup_logging

logger = setup_logging("app")

@broker.task(schedule=[
    {"cron": "0 0 0 * * *"}
            ])
async def upload_task(service: FileUploadService = TaskiqDepends(get_file_upload_service)):
    try:
        logger.info("Starting cleanup-uploads(cron task)")

        deleted_count = await service.cleanup_uploads()

        logger.info("Deleted cleanup-uploads %d(cron task)", deleted_count)

        return deleted_count
    except Exception as e:
        logger.error("Error during upload_task: %s", e)
        return 0