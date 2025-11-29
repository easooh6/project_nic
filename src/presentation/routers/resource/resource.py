from fastapi import APIRouter, status, HTTPException, UploadFile, File, Depends
from src.domain.services.resource_service import ResourceService
from src.presentation.routers.resource.response.resource_responses import ResourceResponse
from src.presentation.routers.resource.response.resource_responses import UploadFileResponse
from src.presentation.routers.resource.request.resource_requests import ResourceCreateRequest
from src.presentation.di.service.auth.verify import get_verify_access
from src.domain.dto.auth.token import TokenDTO

router = APIRouter()

@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    resource_data: ResourceCreateRequest,
    user: TokenDTO = Depends(get_verify_access)
):
    try:
        service = ResourceService()
        resource = await service.create(resource_data)
        return resource
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.post("/{resource_id}/upload-file", response_model=UploadFileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file_to_resource(
    resource_id: int, 
    file: UploadFile = File(...),
    user: TokenDTO = Depends(get_verify_access)
):
    try:
        service = ResourceService()
        uploaded_file = await service.upload_file(resource_id, file, user.sub)
        return uploaded_file
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed:{e}")

@router.get("/{resource_id}", response_model=ResourceResponse, status_code=status.HTTP_200_OK)
async def get_resource_by_id(resource_id: int):
    try:
        service = ResourceService()
        resource = await service.get_by_id(resource_id)
        return resource
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error:{e}")

@router.get("/", response_model=list[ResourceResponse], status_code=status.HTTP_200_OK)
async def get_all_resources():
    try:
        service = ResourceService()
        resources = await service.get_all()
        return resources
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")