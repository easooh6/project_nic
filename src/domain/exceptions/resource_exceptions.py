from fastapi import HTTPException, status

class ResourceNotFoundException(HTTPException):
    def __init__(self, resource_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found"
        )

class FileUploadException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File upload failed: {message}"
        )

class ResourceCreationException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Resource creation failed: {message}"
        )