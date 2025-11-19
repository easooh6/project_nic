
class BaseAuthException(Exception):
    pass

class RefreshRevokedException(BaseAuthException):
    
    def __init__(self):
        super().__init__("Refresh expired")

class RefreshExpiredException(BaseAuthException):
    
    def __init__(self):
        super().__init__("Refresh expired")

class RefreshNotFoundException(BaseAuthException):
    
    def __init__(self):
        super().__init__("Refresh not found")