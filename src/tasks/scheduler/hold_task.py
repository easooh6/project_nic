from src.tasks.broker import broker
from taskiq import TaskiqDepends
from src.domain.upload.file_upload import FileUploadService
from src.logger.logger import setup_logging

logger = setup_logging("app")

@broker.task
async def hold_task():
    pass
