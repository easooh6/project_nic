class BaseUserException(Exception):
    pass

class UserNotExistsException(BaseUserException):

    def __init__(self):
        super().__init__("User not exists")