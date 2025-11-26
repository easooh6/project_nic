import bcrypt
import hashlib

class Hasher:
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def hash_token(token: str) -> str:
        hashed = hashlib.sha256(token.encode('utf-8')).hexdigest()
        return hashed

    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))