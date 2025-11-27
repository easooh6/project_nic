from celery import Celery
from src.infrastructure.settings.settings import settings

celery_app = Celery(
    "app",                     
    broker=settings.redis.REDIS_URL,    
    backend=settings.redis.REDIS_URL,   
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
