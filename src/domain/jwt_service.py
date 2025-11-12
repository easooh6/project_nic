from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from jose import jwt, JWTError
from src.infrastructure.settings.auth import auth_settings

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire
    }
    token = jwt.encode(payload, auth_settings.JWT_SECRET_KEY, algorithm=auth_settings.JWT_ALGORITHM)
    return token

def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, auth_settings.JWT_SECRET_KEY, algorithms=[auth_settings.JWT_ALGORITHM])
    except JWTError as e:
        raise ValueError("Invalid or expired tokem") from e
    if payload.get("type") != "access":
        raise ValueError("Invalid type")
    
    sub = payload.get("sub")
    if sub is None:
        raise ValueError("Missing subject")
    return payload