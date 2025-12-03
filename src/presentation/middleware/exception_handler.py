from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions.auth.auth import (BaseAuthException, EmailAlreadyExistsException,
                                            RefreshNotFoundException, RefreshExpiredException,
                                            RefreshRevokedException)
from src.domain.exceptions.user.user import (UserNotExistsException, UserStateException,
                                             BaseUserException, RoleException)
from src.logger.logger import setup_logging

logger_app = setup_logging("app")
logger_db = setup_logging("db")
logger_redis = setup_logging("redis")

def setup_exception_handler(app: FastAPI):
    
    @app.exception_handler(EmailAlreadyExistsException)
    async def email_already_exists_handler(request: Request, exc: EmailAlreadyExistsException):
        logger_app.warning("Email already exists: %s | URL: %s %s | IP: %s",
                    str(exc), request.method, request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": str(exc)}
        )

    @app.exception_handler(RefreshNotFoundException)
    async def refresh_not_found_handler(request: Request, exc: RefreshNotFoundException):
        logger_app.warning("Refresh token not found: %s | URL: %s %s | IP: %s",
                    str(exc), request.method, request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)}
        )

    @app.exception_handler(RefreshExpiredException)
    async def refresh_expired_handler(request: Request, exc: RefreshExpiredException):
        logger_app.warning("Refresh token expired: %s | URL: %s %s | IP: %s",
                    str(exc), request.method, request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)}
        )

    @app.exception_handler(RefreshRevokedException)
    async def refresh_revoked_handler(request: Request, exc: RefreshRevokedException):
        logger_app.warning("Refresh token revoked: %s | URL: %s %s | IP: %s",
                    str(exc), request.method, request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)}
        )

    @app.exception_handler(UserNotExistsException)
    async def user_not_exists_handler(request: Request, exc: UserNotExistsException):
        logger_app.warning("User not exists: %s | URL: %s %s | IP: %s",
                    str(exc), request.method, request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)}
        )

    @app.exception_handler(UserStateException)
    async def user_state_handler(request: Request, exc: UserStateException):
        logger_app.warning("User state exception: %s | URL: %s %s | IP: %s",
                    str(exc), request.method, request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": str(exc)}
        )

    @app.exception_handler(RoleException)
    async def role_exception_handler(request: Request, exc: RoleException):
        logger_app.warning("Role exception: %s | URL: %s %s | IP: %s",
                    str(exc), request.method, request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": str(exc)}
        )

    @app.exception_handler(BaseAuthException)
    async def base_auth_exception_handler(request: Request, exc: BaseAuthException):
        logger_app.error("Auth exception: %s | URL: %s %s | IP: %s",
                    str(exc), request.method, request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)}
        )

    @app.exception_handler(BaseUserException)
    async def base_user_exception_handler(request: Request, exc: BaseUserException):
        logger_app.error("User exception: %s | URL: %s %s | IP: %s",
                    str(exc), request.method, request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger_app.error("Unhandled exception: %s | URL: %s %s | IP: %s", 
                    str(exc), request.method, request.url, request.client.host, 
                    exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An unexpected error occurred. Our admins are working on it."}
        )