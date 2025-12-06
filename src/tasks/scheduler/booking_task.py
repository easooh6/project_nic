from src.tasks.broker import broker

@broker.task
async def booking_task():
    pass

