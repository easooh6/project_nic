from pydantic import BaseModel

class ResourceResponse(BaseModel):
    id: int
    name: str
    location: str
    capacity: int
    file_path: str | None
    is_active: bool

    class Config:
        from_attributes = True

class UploadFileResponse(BaseModel):
    id: int
    path: str
    size_bytes: int
    mime: str

    class Config:
        from_attributes = True