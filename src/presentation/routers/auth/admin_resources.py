from fastapi import APIRouter, Depends, HTTPException, status

from src.domain.admin.dto import (
    AdminResourceCreate,
    AdminResourceUpdate,
    AdminResourceRead,
)
from src.domain.admin.services import AdminResourceService

from src.presentation.di.service.auth.verify import get_verify_admin  
from src.domain.dto.auth.token import TokenDTO            


router = APIRouter(
    prefix="/resources",
    tags=["admin-resources"],
)


@router.post(
    "",
    response_model=AdminResourceRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_resource(
    body: AdminResourceCreate,
    admin: TokenDTO = Depends(get_verify_admin),
):
    service = AdminResourceService()
    resource = await service.create_resource(body)
    return resource


@router.put(
    "/{resource_id}",
    response_model=AdminResourceRead,
    status_code=status.HTTP_200_OK,
)
async def update_resource(
    resource_id: int,
    body: AdminResourceUpdate,
    admin: TokenDTO = Depends(get_verify_admin),
):
    service = AdminResourceService()
    resource = await service.update_resource(
        resource_id=resource_id,
        data=body,
        affected_dates=None,  
    )
    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )
    return resource


@router.delete(
    "/{resource_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_resource(
    resource_id: int,
    admin: TokenDTO = Depends(get_verify_admin),
):
    service = AdminResourceService()
    success = await service.delete_resource(
        resource_id=resource_id,
        affected_dates=None,
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )
