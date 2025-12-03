
class BaseAuthException(Exception):
    pass

class RefreshRevokedException(BaseAuthException):
    
    def __init__(self):
        super().__init__("Refresh revoked")

class RefreshExpiredException(BaseAuthException):
    
    def __init__(self):
        super().__init__("Refresh expired")

class RefreshNotFoundException(BaseAuthException):
    
    def __init__(self):
        super().__init__("Refresh not found")

class EmailAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("User with this email already exists")


class InvalidResetTokenException(BaseAuthException):
    def __init__(self):
        super().__init__("Invalid reset token")


class ResetTokenNotFoundException(BaseAuthException):
    def __init__(self):
        super().__init__("Reset token not found or expired")
