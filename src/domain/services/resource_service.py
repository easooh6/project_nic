import json
from fastapi import UploadFile
from src.infrastructure.db.repositories.resource import ResourceRepository
from src.infrastructure.db.repositories.file_upload import FileUploadRepository
from src.infrastructure.redis.repository import RedisRepository

from src.presentation.routers.resource.response.resource_responses import ResourceResponse, UploadFileResponse 
from src.presentation.routers.resource.request.resource_requests import ResourceCreateRequest

from src.domain.exceptions.resource_exceptions import ResourceNotFoundException, FileUploadException, ResourceCreationException
from src.logger.logger import setup_logging

logger = setup_logging("app")


class ResourceService:
    CACHE_TTL = 60  

    def __init__(self):
        self.repo = ResourceRepository()
        self.file_repo = FileUploadRepository()
        self.redis = RedisRepository()

    async def create(self, data: ResourceCreateRequest):
        try:
            resource = await self.repo.create(
                name=data.name,
                location=data.location,
                capacity=data.capacity,
                file_path=data.file_path
            )
        except Exception as e:
            raise ResourceCreationException(str(e))

        await self.redis.delete("resources:all")

        logger.debug("Created new resource")
        return ResourceResponse.model_validate(resource)


    async def get_all(self):
        cache_key = "resources:all"

        cached = await self.redis.get(cache_key)
        if cached:
            logger.debug("Loaded all resources from redis cache")
            items = json.loads(cached)
            return [ResourceResponse(**item) for item in items]

        resources = await self.repo.get_all()
        items = [ResourceResponse.model_validate(r).model_dump() for r in resources]

        await self.redis.set(cache_key, json.dumps(items), ttl=self.CACHE_TTL)

        logger.debug("Loaded all resources from DB & cached them")
        return [ResourceResponse(**item) for item in items]


    async def get_by_id(self, resource_id: int):
        cache_key = f"resource:{resource_id}"

        cached = await self.redis.get(cache_key)
        if cached:
            logger.debug("Loaded resource from redis cache")
            return ResourceResponse(**json.loads(cached))

        resource = await self.repo.get_by_id(resource_id)
        if resource is None:
            raise ResourceNotFoundException(resource_id)

        dto = ResourceResponse.model_validate(resource)
        await self.redis.set(cache_key, dto.model_dump_json(), ttl=self.CACHE_TTL)

        logger.debug("Loaded resource from DB and cached it")
        return dto

    async def upload_file(self, resource_id: int, file: UploadFile, user_id: int):
        resource = await self.repo.get_by_id(resource_id)
        if resource is None:
            raise ResourceNotFoundException(resource_id)

        try:
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
            await self.repo.update_file_path(resource_id, save_path)

        except Exception as e:
            raise FileUploadException(str(e))

        await self.redis.delete(f"resource:{resource_id}")
        await self.redis.delete("resources:all")

        logger.debug(f"File uploaded for resource {resource_id}")
        return UploadFileResponse.model_validate(new_file)
