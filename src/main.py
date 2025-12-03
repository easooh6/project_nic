from fastapi import FastAPI
from src.presentation.routers.auth.auth import router as auth_router
from src.presentation.routers.auth.admin_resources import router as admin_resources_router
from src.presentation.routers.resource.resource import router as resource_router
from contextlib import asynccontextmanager
from src.infrastructure.redis.client import init_redis_client, close_redis_client
from src.infrastructure.db.db import init_db, close_db
from src.presentation.middleware.exception_handler import setup_exception_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_redis_client()
    yield
    await close_db()
    await close_redis_client()

app = FastAPI(
    lifespan=lifespan,
    title="NIC project",
    description="API for NIC project",
    version="0.1.0"
)

setup_exception_handler(app)
# пример подключения роутеров
# app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# app.include_router(user_router, prefix="/user", tags=["User Profile"])
# app.include_router(search_router, prefix="/search", tags=["Search"])

app.include_router(auth_router, prefix="/auth",tags=["Authentication"])
app.include_router(admin_resources_router)
app.include_router(resource_router, prefix="/resources", tags=["Resources"])

