from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class Intent(str, Enum):
    STORE_OBJECT = "StoreObject"
    MOVE_OBJECT = "MoveObject"
    DELETE_OBJECT = "DeleteObject"
    FIND_OBJECT = "FindObject"
    LIST_OBJECTS = "ListObjects"
    LIST_ROOM = "ListRoom"
    UPDATE_DESCRIPTION = "UpdateDescription"
    UNKNOWN = "Unknown"

class ExtractedEntities(BaseModel):
    object_name: Optional[str] = None
    room_name: Optional[str] = None
    furniture_name: Optional[str] = None
    container_name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None

class AIIntentResponse(BaseModel):
    intent: Intent
    entities: ExtractedEntities
    confidence: float
    reasoning: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    intent: Optional[Intent] = None
    session_id: int
