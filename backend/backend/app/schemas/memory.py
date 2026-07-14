from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Room Schemas
class RoomBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# Furniture Schemas
class FurnitureBase(BaseModel):
    name: str
    type: Optional[str] = None

class FurnitureCreate(FurnitureBase):
    room_id: int

class FurnitureResponse(FurnitureBase):
    id: int
    room_id: int

    class Config:
        from_attributes = True

# Container Schemas
class ContainerBase(BaseModel):
    name: str

class ContainerCreate(ContainerBase):
    furniture_id: int

class ContainerResponse(ContainerBase):
    id: int
    furniture_id: int

    class Config:
        from_attributes = True

# Location Schemas
class LocationResponse(BaseModel):
    id: int
    room_id: int
    furniture_id: Optional[int] = None
    container_id: Optional[int] = None

    class Config:
        from_attributes = True

# Object Schemas
class StoredObjectBase(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None

class StoredObjectCreate(StoredObjectBase):
    room_id: int
    furniture_id: Optional[int] = None
    container_id: Optional[int] = None

class StoredObjectResponse(StoredObjectBase):
    id: int
    user_id: int
    current_location_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# History Schemas
class MemoryHistoryResponse(BaseModel):
    id: int
    object_id: int
    previous_location: Optional[str]
    new_location: Optional[str]
    timestamp: datetime
    reason: Optional[str]

    class Config:
        from_attributes = True
