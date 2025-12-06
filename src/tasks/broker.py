from taskiq_redis import RedisStreamBroker
from src.infrastructure.settings.settings import settings

broker = RedisStreamBroker(settings.redis.REDIS_BROKER_URL)