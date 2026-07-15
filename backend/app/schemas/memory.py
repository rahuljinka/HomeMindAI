from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- Minimal Schemas ---

class HouseMinimalResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    user_id: int

    class Config:
        from_attributes = True

class RoomMinimalResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    user_id: int
    house_id: Optional[int] = None
    house: Optional[HouseMinimalResponse] = None

    class Config:
        from_attributes = True

class FurnitureMinimalResponse(BaseModel):
    id: int
    name: str
    type: Optional[str] = None
    room_id: int

    class Config:
        from_attributes = True

class ContainerMinimalResponse(BaseModel):
    id: int
    name: str
    furniture_id: int

    class Config:
        from_attributes = True

# --- Full Schemas ---

class FurnitureResponse(FurnitureMinimalResponse):
    containers: List[ContainerMinimalResponse] = []

    class Config:
        from_attributes = True

class RoomResponse(RoomMinimalResponse):
    furniture: List[FurnitureResponse] = []

    class Config:
        from_attributes = True

class HouseResponse(HouseMinimalResponse):
    created_at: datetime
    updated_at: datetime
    rooms: List[RoomResponse] = []

    class Config:
        from_attributes = True

# --- Create Schemas ---

class HouseCreate(BaseModel):
    name: str
    description: Optional[str] = None

class RoomCreate(BaseModel):
    name: str
    description: Optional[str] = None
    house_id: Optional[int] = None

class FurnitureCreate(BaseModel):
    name: str
    type: Optional[str] = None
    room_id: int

class ContainerCreate(BaseModel):
    name: str
    furniture_id: int

# --- Location & Object Schemas ---

class LocationResponse(BaseModel):
    id: int
    room: Optional[RoomMinimalResponse] = None
    furniture: Optional[FurnitureMinimalResponse] = None
    container: Optional[ContainerMinimalResponse] = None

    class Config:
        from_attributes = True

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
    current_location: Optional[LocationResponse] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class MemoryHistoryResponse(BaseModel):
    id: int
    object_id: int
    previous_location: Optional[str]
    new_location: Optional[str]
    timestamp: datetime
    reason: Optional[str]

    class Config:
        from_attributes = True

# Update forward refs
RoomResponse.update_forward_refs()
HouseResponse.update_forward_refs()
