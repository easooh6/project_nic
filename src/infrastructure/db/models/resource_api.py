
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.db import get_db_session
from src.infrastructure.db.models.resource_repo import ResourceRepository

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

repo = ResourceRepository()

@app.post("/resources")
async def create_resource(name: str, location: str, capacity: int, file_path: str | None = None, db: AsyncSession = Depends(get_db_session)):
    resource = await repo.create(db, name, location, capacity, file_path)
    return {"id": resource.id, "name": resource.name}

@app.get("/resources/{resource_id}")
async def get_resource(resource_id: int, db: AsyncSession = Depends(get_db_session)):
    resource = await repo.get_by_id(db, resource_id)
    return await repo.get_all(db)

@app.get("/resources/filter")
async def filter_resources(capacity: int | None = None, location: str | None = None, db: AsyncSession = Depends(get_db_session)):
    return await repo.filter(db, capacity, location)

@app.put("/resources/{resource_id}")
async def update_resource( resource_id: int, data: dict, db: AsyncSession = Depends(get_db_session)):
    updated = await repo.update(db, resource_id, data)
    if not updated: 
        raise HTTPException(status_code=404, detail="resource not found")
    return updated

@app.delete("/resorces/{resource_id}")
async def delete_resource(resource_id: int, db: AsyncSession = Depends(get_db_session)):
    success = await repo.delete(db, resource_id)
    if not success:
        raise HTTPException(status_code=404, detail="resource not found")
    return{"status": "deleted"}