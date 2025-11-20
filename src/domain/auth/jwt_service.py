from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from jose import jwt, JWSError, JWTError
from jose.exceptions import JWTClaimsError, JWEError, ExpiredSignatureError
from src.infrastructure.settings.settings import settings
from src.domain.enums.role import RoleEnum
from src.domain.entities.refresh import RefreshEntity
from src.domain.exceptions.auth.auth import RefreshExpiredException, RefreshRevokedException

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
        except ExpiredSignatureError:
            raise ExpiredSignatureError("Access token has expired")
        except JWTClaimsError as e:
            raise JWTClaimsError(f"Invalid claims in token{e}") from e
        except JWSError:
            raise JWSError("Invalid token signature")
        except JWEError:
            raise JWEError("Invalid token decryption")
        except JWTError as e:
            raise JWTError(f"Invalid token: {e}") from e
        
        if payload.get("type") != "access":
            raise JWTClaimsError("Invalid token type")
        if "sub" not in payload:
            raise JWTClaimsError("Missing subject")
        
        role = payload.get("role")
        payload["sub"] = int(payload["sub"])
        try:
            RoleEnum(role)
        except JWTClaimsError as e:
            raise JWTClaimsError("Invalid role value in token")
        return payload

class RefreshValidator:

    @staticmethod
    def validate(entity: RefreshEntity):
        if entity.revoked:
            raise RefreshRevokedException
        now = datetime.now(timezone.utc)
        if entity.expires_at < now:
            raise RefreshExpiredException
        