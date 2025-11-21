from src.infrastructure.utils.password import hash_password, verify_password


class HashService:
    def hash(self, value: str) -> str:
        return hash_password(value)

    def verify(self, plain: str, hashed: str) -> bool:
        return verify_password(plain, hashed)
