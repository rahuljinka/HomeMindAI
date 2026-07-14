from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.memory_repository import MemoryRepository
from app.ai.memory.ai_service import AIService
from app.schemas.ai import Intent, AIIntentResponse
from app.models.user import User

class MemoryPipelineService:
    def __init__(self, db: AsyncSession, ai_service: AIService):
        self.db = db
        self.ai_service = ai_service
        self.repo = MemoryRepository(db)

    async def process_message(self, user: User, message: str, session_id: int):
        # 1. Intent Detection & Entity Extraction
        ai_intent = await self.ai_service.detect_intent(message)
        
        context_info = ""
        
        # 2. Database Update / Query based on intent
        if ai_intent.intent == Intent.STORE_OBJECT:
            context_info = await self._handle_store(user, ai_intent)
        elif ai_intent.intent == Intent.FIND_OBJECT:
            context_info = await self._handle_find(user, ai_intent)
        # ... other intents ...
        else:
            context_info = "I'm not sure how to help with that yet."

        # 3. Generate AI Response
        ai_response = await self.ai_service.generate_response(message, context_info)
        
        return ai_response, ai_intent.intent

    async def _handle_store(self, user: User, ai_intent: AIIntentResponse):
        entities = ai_intent.entities
        if not entities.object_name or not entities.room_name:
            return "Missing object name or room name for storing."
        
        # Simple logic: find or create room, then store object
        rooms = await self.repo.get_rooms(user.id)
        room = next((r for r in rooms if r.name.lower() == entities.room_name.lower()), None)
        
        if not room:
            room = await self.repo.create_room(user.id, entities.room_name)
            
        location = await self.repo.get_or_create_location(room.id)
        obj = await self.repo.create_object(user.id, entities.object_name, entities.category, entities.description)
        obj.current_location_id = location.id
        await self.db.commit()
        
        return f"Stored {entities.object_name} in {entities.room_name}."

    async def _handle_find(self, user: User, ai_intent: AIIntentResponse):
        entities = ai_intent.entities
        if not entities.object_name:
            return "Missing object name to search for."
            
        objects = await self.repo.get_objects(user.id)
        obj = next((o for o in objects if o.name.lower() == entities.object_name.lower()), None)
        
        if not obj:
            return f"I couldn't find any information about {entities.object_name}."
            
        # Get location details (simplified)
        return f"Your {obj.name} is in its recorded location."
