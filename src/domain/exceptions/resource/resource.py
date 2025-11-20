class BaseResourceException(Exception):
    pass

class ResourceNotFoundException(BaseResourceException):
    def __init__(self):
        super().__init__("Resource not found")

class ResourceInactiveException(BaseResourceException):
    def __init__(self):
        super().__init__("Resource is inactive")

class ResourceInvalidDataException(BaseResourceException):
    def __init__(self, field: str):
        super().__init__(f"Invalid value for field '{field}'")