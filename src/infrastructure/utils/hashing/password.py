import bcrypt
import hashlib

class Hasher:
<<<<<<< HEAD
    def hash_password(password: str) -> str:
=======
    def hash_password(self, password: str) -> str:
>>>>>>> feature/logout_bug_fix
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

<<<<<<< HEAD
    def hash_token(token: str) -> str:
        hashed = hashlib.sha256(token.encode('utf-8')).hexdigest()
        return hashed

    def verify_password(password: str, hashed_password: str) -> bool:
=======
    def hash_token(self, token: str) -> str:
        hashed = hashlib.sha256(token.encode('utf-8')).hexdigest()
        return hashed

    def verify_password(self, password: str, hashed_password: str) -> bool:
>>>>>>> feature/logout_bug_fix
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))