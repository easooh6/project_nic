from .auth_requests import LoginRequest, RegisterRequest
from .forgot_password import ForgotPasswordRequest
from .reset_password import ResetPasswordRequest

__all__ = [
    "LoginRequest",
    "RegisterRequest",
    "ForgotPasswordRequest",
    "ResetPasswordRequest"
]
