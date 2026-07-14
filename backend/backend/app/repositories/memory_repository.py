from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from backend.app.models.memory import Room, Furniture, Container, Location, StoredObject, MemoryHistory, ObjectAlias, ObjectPhoto

class MemoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Room Methods
    async def create_room(self, user_id: int, name: str, description: Optional[str] = None):
        room = Room(user_id=user_id, name=name, description=description)
        self.db.add(room)
        await self.db.flush()
        return room

    async def get_rooms(self, user_id: int) -> List[Room]:
        result = await self.db.execute(select(Room).filter(Room.user_id == user_id))
        return result.scalars().all()

    async def get_room_by_name(self, user_id: int, name: str) -> Optional[Room]:
        result = await self.db.execute(select(Room).filter(Room.user_id == user_id, Room.name.ilike(name)))
        return result.scalars().first()

    # Furniture Methods
    async def get_or_create_furniture(self, room_id: int, name: str):
        result = await self.db.execute(select(Furniture).filter(Furniture.room_id == room_id, Furniture.name.ilike(name)))
        furniture = result.scalars().first()
        if not furniture:
            furniture = Furniture(room_id=room_id, name=name)
            self.db.add(furniture)
            await self.db.flush()
        return furniture

    # Container Methods
    async def get_or_create_container(self, furniture_id: int, name: str):
        result = await self.db.execute(select(Container).filter(Container.furniture_id == furniture_id, Container.name.ilike(name)))
        container = result.scalars().first()
        if not container:
            container = Container(furniture_id=furniture_id, name=name)
            self.db.add(container)
            await self.db.flush()
        return container

    # Location Methods
    async def get_or_create_location(self, room_id: int, furniture_id: Optional[int] = None, container_id: Optional[int] = None):
        query = select(Location).filter(
            Location.room_id == room_id, 
            Location.furniture_id == furniture_id, 
            Location.container_id == container_id
        )
        result = await self.db.execute(query)
        location = result.scalars().first()
        if not location:
            location = Location(room_id=room_id, furniture_id=furniture_id, container_id=container_id)
            self.db.add(location)
            await self.db.flush()
        return location

    # Object Methods
    async def create_object(self, user_id: int, name: str, category: Optional[str] = None, description: Optional[str] = None):
        obj = StoredObject(user_id=user_id, name=name, category=category, description=description)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def get_objects(self, user_id: int) -> List[StoredObject]:
        result = await self.db.execute(
            select(StoredObject)
            .filter(StoredObject.user_id == user_id)
            .options(
                selectinload(StoredObject.current_location).selectinload(Location.room),
                selectinload(StoredObject.current_location).selectinload(Location.furniture),
                selectinload(StoredObject.current_location).selectinload(Location.container)
            )
        )
        return result.scalars().all()

    async def get_object_by_name(self, user_id: int, name: str) -> Optional[StoredObject]:
        result = await self.db.execute(
            select(StoredObject)
            .filter(StoredObject.user_id == user_id, StoredObject.name.ilike(name))
            .options(
                selectinload(StoredObject.current_location).selectinload(Location.room),
                selectinload(StoredObject.current_location).selectinload(Location.furniture),
                selectinload(StoredObject.current_location).selectinload(Location.container)
            )
        )
        return result.scalars().first()

    async def search_objects(self, user_id: int, query: str) -> List[StoredObject]:
        search_query = f"%{query}%"
        result = await self.db.execute(
            select(StoredObject)
            .filter(
                StoredObject.user_id == user_id,
                or_(
                    StoredObject.name.ilike(search_query),
                    StoredObject.description.ilike(search_query),
                    StoredObject.category.ilike(search_query)
                )
            )
            .options(
                selectinload(StoredObject.current_location).selectinload(Location.room),
                selectinload(StoredObject.current_location).selectinload(Location.furniture),
                selectinload(StoredObject.current_location).selectinload(Location.container)
            )
        )
        return result.scalars().all()

    # History Methods
    async def create_history(self, object_id: int, previous_location: str, new_location: str, reason: Optional[str] = None):
        history = MemoryHistory(
            object_id=object_id,
            previous_location=previous_location,
            new_location=new_location,
            reason=reason
        )
        self.db.add(history)
        await self.db.flush()
        return history

    async def get_history(self, object_id: int) -> List[MemoryHistory]:
        result = await self.db.execute(
            select(MemoryHistory)
            .filter(MemoryHistory.object_id == object_id)
            .order_by(MemoryHistory.timestamp.desc())
        )
        return result.scalars().all()
