from taskiq_redis import ListRedisScheduleSource
from src.infrastructure.settings.settings import settings
from taskiq import TaskiqScheduler
from src.tasks.scheduler.upload_task import upload_task
from src.tasks.scheduler.hold_task import release_holds
from src.tasks.broker import broker

release_source = ListRedisScheduleSource(settings.redis.REDIS_SCHEDULER_URL,
                                          prefix="release-holds")
uploads_source = ListRedisScheduleSource(settings.redis.REDIS_SCHEDULER_URL,
                                          prefix="cleanup-uploads")
booking_source = ListRedisScheduleSource(settings.redis.REDIS_SCHEDULER_URL,
                                         prefix="archive-bookings")
uploads_source.add_schedule(upload_task)
release_source.add_schedule(release_holds)

scheduler = TaskiqScheduler(broker=broker,
                            sources=[release_source,uploads_source,booking_source])