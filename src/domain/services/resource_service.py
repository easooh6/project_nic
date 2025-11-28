from src.infrastructure.db.repositories.resource import ResourceRepository
from src.infrastructure.db.repositories.file_upload import FileUploadRepository
from src.presentation.responses.resource_responses import ResourceResponse
from src.presentation.responses.resource_responses import UploadFileResponse
from src.presentation.requests.resource_requests import ResourceCreateRequest
from src.logger.logger import setup_logging
from fastapi import UploadFile

logger = setup_logging("app")

class ResourceService():
    def __init__(self):
        self.repo = ResourceRepository()
        self.file_repo = FileUploadRepository()
    
    async def create(self, data: ResourceCreateRequest):
        resource = await self.repo.create(
            name=data.name, 
            location=data.location,
            capacity=data.capacity,
            file_path=data.file_path
        )
        logger.debug("Creating new resource")
        return ResourceResponse.model_validate(resource)
    
    async def get_all(self):
        resources = await self.repo.get_all()
        logger.debug("Returning all resources")
        return [ResourceResponse.model_validate(r) for r in resources]
    
    async def get_by_id(self, resource_id: int):
        resource = await self.repo.get_by_id(resource_id)
        if resource is None:
            raise ValueError("Resource not found")
        logger.debug(f"Getting resource id {resource_id}")
        return ResourceResponse.model_validate(resource)

    async def upload_file(self, resource_id: int, file: UploadFile, user_id: int):
        resource = await self.repo.get_by_id(resource_id)
        if resource is None:
            raise ValueError("Resource not found")
        
        save_path = f"/app/uploads/{file.filename}"
        
        content = await file.read()
        with open(save_path, "wb") as f:
            f.write(content)

        new_file = await self.file_repo.create(
            path=save_path,
            size_bytes=len(content),
            mime=file.content_type,
            owner_user_id=user_id 
        )
        
        logger.debug(f"File uploaded to resource {resource_id}")
        return UploadFileResponse.model_validate(new_file)