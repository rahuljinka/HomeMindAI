from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database.session import get_db
from app.schemas.memory import HouseCreate, HouseResponse
from app.repositories.memory_repository import MemoryRepository
from app.middleware.auth import get_current_user
from app.models.user import User
from sqlalchemy.orm import selectinload
from app.models.memory import House, Room, Furniture

router = APIRouter(prefix="/locations", tags=["locations"])

@router.post("/", response_model=HouseResponse)
async def create_location(
    house: HouseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = MemoryRepository(db)
    new_house = await repo.create_house(user_id=current_user.id, name=house.name, description=house.description)
    await db.commit()
    await db.refresh(new_house)
    # Refresh with relationships
    result = await db.execute(
        select(House)
        .filter(House.id == new_house.id)
        .options(
            selectinload(House.rooms)
            .selectinload(Room.furniture)
            .selectinload(Furniture.containers)
        )
    )
    return result.scalars().first()

@router.get("/", response_model=List[HouseResponse])
async def list_locations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = MemoryRepository(db)
    return await repo.get_houses(user_id=current_user.id)

@router.get("/{location_id}", response_model=HouseResponse)
async def get_location(
    location_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(House)
        .filter(House.id == location_id, House.user_id == current_user.id)
        .options(
            selectinload(House.rooms)
            .selectinload(Room.furniture)
            .selectinload(Furniture.containers)
        )
    )
    house = result.scalars().first()
    if not house:
        raise HTTPException(status_code=404, detail="Location not found")
    return house
