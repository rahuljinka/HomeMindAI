from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.session import get_db
from app.schemas.memory import RoomCreate, RoomResponse
from app.repositories.memory_repository import MemoryRepository
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("/", response_model=RoomResponse)
async def create_room(
    room: RoomCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = MemoryRepository(db)
    return await repo.create_room(user_id=current_user.id, name=room.name, description=room.description)

@router.get("/", response_model=List[RoomResponse])
async def list_rooms(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = MemoryRepository(db)
    return await repo.get_rooms(user_id=current_user.id)

@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = MemoryRepository(db)
    room = await repo.get_room(room_id=room_id, user_id=current_user.id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room
