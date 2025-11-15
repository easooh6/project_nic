
class BaseAuthException(Exception):
    pass

class RoleException(BaseAuthException):

    def __init__(self):
        super().__init__("Not correct role")

class UserNotExistsException(BaseAuthException):

    def __init__(self):
        super().__init__("User not exists")