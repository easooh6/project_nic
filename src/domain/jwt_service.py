from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from jose import jwt, JWTError
from src.infrastructure.settings.settings import settings
from src.domain.enums.role import RoleEnum

class JWT:
    def __init__(self):
        self.secret_key = settings.auth.JWT_SECRET_KEY
        self.algorithm = settings.auth.JWT_ALGORITHM
        self.access_expire_min = settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, user_id: int, role: RoleEnum) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_expire_min)
        payload: Dict[str, Any] = {
            "sub": str(user_id),
            "role": role.value,
            "type": "access",
            "exp": expire
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_access_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError as e:
            raise ValueError("Invalid or expired token") from e
        
        if payload.get("type") != "access":
            raise ValueError("Invalid token type")
        if "sub" not in payload:
            raise ValueError("Missing subject")
        
        role = payload.get("role")
        if role not in RoleEnum._value2member_map_:
            raise ValueError("Invalid role value in token")
        return payload
