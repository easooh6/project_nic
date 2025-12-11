from taskiq_redis import ListRedisScheduleSource
from src.infrastructure.settings.settings import settings
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from src.tasks.broker import broker

label_source = LabelScheduleSource(broker)

#release_holds_source = ListRedisScheduleSource(settings.redis.REDIS_SCHEDULER_URL, prefix="release-holds")
#cleanup_uploads_source = ListRedisScheduleSource(settings.redis.REDIS_SCHEDULER_URL, prefix="cleanup-uploads")
#archive_bookings_source = ListRedisScheduleSource(settings.redis.REDIS_SCHEDULER_URL, prefix="archive-bookings")

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[label_source]
)