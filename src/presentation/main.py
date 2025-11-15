from fastapi import FastAPI
app = FastAPI(
    title="NIC project",
    description="API for NIC project",
    version="0.1.0"
)

# пример подключения роутеров
# app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# app.include_router(user_router, prefix="/user", tags=["User Profile"])
# app.include_router(search_router, prefix="/search", tags=["Search"])