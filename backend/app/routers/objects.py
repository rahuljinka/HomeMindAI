from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.session import get_db
from app.schemas.memory import StoredObjectCreate, StoredObjectResponse
from app.repositories.memory_repository import MemoryRepository
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/objects", tags=["objects"])

@router.post("/", response_model=StoredObjectResponse)
async def create_object(
    obj: StoredObjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = MemoryRepository(db)
    # Check if room exists
    room = await repo.get_room(obj.room_id, current_user.id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Get or create location
    location = await repo.get_or_create_location(
        room_id=obj.room_id,
        furniture_id=obj.furniture_id,
        container_id=obj.container_id
    )
    
    new_obj = await repo.create_object(
        user_id=current_user.id,
        name=obj.name,
        category=obj.category,
        description=obj.description
    )
    new_obj.current_location_id = location.id
    await db.commit()
    await db.refresh(new_obj)
    return new_obj

@router.get("/", response_model=List[StoredObjectResponse])
async def list_objects(
    q: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = MemoryRepository(db)
    if q:
        return await repo.search_objects(user_id=current_user.id, query=q)
    return await repo.get_objects(user_id=current_user.id)

@router.get("/{object_id}", response_model=StoredObjectResponse)
async def get_object(
    object_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = MemoryRepository(db)
    obj = await repo.get_object(object_id=object_id, user_id=current_user.id)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    return obj
