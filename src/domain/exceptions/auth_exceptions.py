class AuthException(Exception):
    def __init__(self, message: str = "Authentication error"):
        self.message = message
        super().__init__(self.message)


class UserNotExistsException(AuthException):
    def __init__(self, message: str = "User does not exist"):
        super().__init__(message)


class UserStateException(AuthException):
    def __init__(self, message: str = "User account is disabled"):
        super().__init__(message)


class InvalidCredentialsException(AuthException):
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message)


class EmailAlreadyExistsException(AuthException):
    def __init__(self, message: str = "Email already exists"):
        super().__init__(message)


class InvalidTokenException(AuthException):
    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message)