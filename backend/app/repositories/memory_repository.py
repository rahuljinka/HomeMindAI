from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.models.memory import Room, Furniture, Container, Location, StoredObject, MemoryHistory

class MemoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Room Methods
    async def create_room(self, user_id: int, name: str, description: Optional[str] = None):
        room = Room(user_id=user_id, name=name, description=description)
        self.db.add(room)
        await self.db.commit()
        await self.db.refresh(room)
        return room

    async def get_rooms(self, user_id: int) -> List[Room]:
        result = await self.db.execute(select(Room).filter(Room.user_id == user_id))
        return result.scalars().all()

    async def get_room(self, room_id: int, user_id: int) -> Optional[Room]:
        result = await self.db.execute(select(Room).filter(Room.id == room_id, Room.user_id == user_id))
        return result.scalars().first()

    # Object Methods
    async def create_object(self, user_id: int, name: str, category: Optional[str] = None, description: Optional[str] = None):
        obj = StoredObject(user_id=user_id, name=name, category=category, description=description)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def get_objects(self, user_id: int) -> List[StoredObject]:
        result = await self.db.execute(select(StoredObject).filter(StoredObject.user_id == user_id))
        return result.scalars().all()

    async def get_object(self, object_id: int, user_id: int) -> Optional[StoredObject]:
        result = await self.db.execute(select(StoredObject).filter(StoredObject.id == object_id, StoredObject.user_id == user_id))
        return result.scalars().first()

    # Location Methods
    async def get_or_create_location(self, room_id: int, furniture_id: Optional[int] = None, container_id: Optional[int] = None):
        query = select(Location).filter(Location.room_id == room_id, Location.furniture_id == furniture_id, Location.container_id == container_id)
        result = await self.db.execute(query)
        location = result.scalars().first()
        if not location:
            location = Location(room_id=room_id, furniture_id=furniture_id, container_id=container_id)
            self.db.add(location)
            await self.db.commit()
            await self.db.refresh(location)
        return location
