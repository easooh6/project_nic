from typing import Optional

from pydantic import BaseModel, Field


class AdminResourceCreate(BaseModel):
    name: str = Field(..., description="")
    location: str = Field(..., description="")
    capacity: int = Field(..., ge=1, description="")
    description: Optional[str] = Field(
        default=None,
        description="",
    )


class AdminResourceUpdate(BaseModel):
    name: Optional[str] = Field(default=None, description="")
    location: Optional[str] = Field(default=None, description="")
    capacity: Optional[int] = Field(
        default=None,
        ge=1,
        description="",
    )
    description: Optional[str] = Field(
        default=None,
        description="",
    )
    is_active: Optional[bool] = Field(
        default=None,
        description="",
    )


class AdminResourceRead(BaseModel):
    id: int
    name: str
    location: str
    capacity: int
    is_active: bool
    file_path: Optional[str] = None
    description: Optional[str] = None
