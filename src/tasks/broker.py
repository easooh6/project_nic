from taskiq_redis import RedisStreamBroker
from src.infrastructure.settings.settings import settings
from src.infrastructure.db.db import init_db, close_db
from taskiq import TaskiqEvents
broker = RedisStreamBroker(settings.redis.REDIS_BROKER_URL)

@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def init(state):
    await init_db()

@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def close(state):
    await close_db()

