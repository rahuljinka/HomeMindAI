from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class Intent(str, Enum):
    STORE_OBJECT = "STORE_OBJECT"
    MOVE_OBJECT = "MOVE_OBJECT"
    FIND_OBJECT = "FIND_OBJECT"
    LIST_OBJECTS = "LIST_OBJECTS"
    DELETE_OBJECT = "DELETE_OBJECT"
    UPDATE_OBJECT = "UPDATE_OBJECT"
    UNKNOWN = "UNKNOWN"

class AIObject(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None

class AILocation(BaseModel):
    house_name: Optional[str] = None
    room: str
    furniture: Optional[str] = None
    container: Optional[str] = None

class AIIntentResponse(BaseModel):
    intent: Intent
    object: Optional[AIObject] = None
    location: Optional[AILocation] = None
    reasoning: Optional[str] = None

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
