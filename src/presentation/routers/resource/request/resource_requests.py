from pydantic import BaseModel

class ResourceCreateRequest(BaseModel):
    name: str
    location: str
    capacity: int
    file_path: str | None
