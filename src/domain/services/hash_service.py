from src.infrastructure.utils.hashing.password import Hasher

class HashService:

    def __init__(self):
        self.hasher = Hasher()

    def hash(self, value: str) -> str:
        return self.hasher.hash_password(value)
    
    def hash_token(self, token: str) -> str:
        return self.hasher.hash_token(token)

    def verify(self, plain: str, hashed: str) -> bool:
        return self.hasher.verify_password(plain, hashed)
