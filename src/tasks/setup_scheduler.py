from taskiq_redis import ListRedisScheduleSource
from src.infrastructure.settings.settings import settings
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from src.tasks.broker import broker

# Импортируем модули с задачами, чтобы они зарегистрировались в брокере
from src.tasks.scheduler.upload_task import cleanup_uploads_task
from src.tasks.scheduler.hold_task import release_holds_task
from src.tasks.scheduler.booking_task import archive_bookings_task

# Источник для задач, определенных через декоратор @broker.task(schedule=[...])
label_source = LabelScheduleSource(broker)

# Источники для динамических задач (если понадобятся в будущем)
release_holds_source = ListRedisScheduleSource(settings.redis.REDIS_SCHEDULER_URL, prefix="release-holds")
cleanup_uploads_source = ListRedisScheduleSource(settings.redis.REDIS_SCHEDULER_URL, prefix="cleanup-uploads")
archive_bookings_source = ListRedisScheduleSource(settings.redis.REDIS_SCHEDULER_URL, prefix="archive-bookings")

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[label_source, release_holds_source, cleanup_uploads_source, archive_bookings_source]
)