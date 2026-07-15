from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.database.session import get_db
from app.schemas.memory import RoomCreate, RoomResponse
from app.repositories.memory_repository import MemoryRepository
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.memory import Room

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("/", response_model=RoomResponse)
async def create_room(
    room: RoomCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = MemoryRepository(db)
    new_room = await repo.create_room(
        user_id=current_user.id, 
        name=room.name, 
        description=room.description,
        house_id=room.house_id
    )
    await db.commit()
    await db.refresh(new_room)
    return new_room

@router.get("/", response_model=List[RoomResponse])
async def list_rooms(
    house_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = MemoryRepository(db)
    return await repo.get_rooms(user_id=current_user.id, house_id=house_id)

@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Room).filter(Room.id == room_id, Room.user_id == current_user.id))
    room = result.scalars().first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room
