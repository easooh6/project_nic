class BaseUserException(Exception):
    pass

class UserNotExistsException(BaseUserException):

    def __init__(self):
        super().__init__("User not exists")

class UserStateException(BaseUserException):

    def __init__(self):
        super().__init__("User's is not active")

class RoleException(BaseUserException):

    def __init__(self):
        super().__init__("Not correct role")
