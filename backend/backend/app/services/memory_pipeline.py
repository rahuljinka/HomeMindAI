from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.repositories.memory_repository import MemoryRepository
from backend.app.ai.memory.ai_service import AIService
from backend.app.schemas.ai import Intent, AIIntentResponse
from backend.app.models.user import User
from backend.app.models.memory import Location

class MemoryPipelineService:
    def __init__(self, db: AsyncSession, ai_service: AIService):
        self.db = db
        self.ai_service = ai_service
        self.repo = MemoryRepository(db)

    async def process_message(self, user: User, message: str, session_id: int):
        # 1. Intent Detection & Entity Extraction
        ai_intent = await self.ai_service.detect_intent(message)
        
        context_info = ""
        
        # 2. Database Operation based on intent
        if ai_intent.intent == Intent.STORE_OBJECT:
            context_info = await self._handle_store(user, ai_intent)
        elif ai_intent.intent == Intent.MOVE_OBJECT:
            context_info = await self._handle_move(user, ai_intent)
        elif ai_intent.intent == Intent.FIND_OBJECT:
            context_info = await self._handle_find(user, ai_intent)
        elif ai_intent.intent == Intent.LIST_OBJECTS:
            context_info = await self._handle_list(user, ai_intent)
        elif ai_intent.intent == Intent.DELETE_OBJECT:
            context_info = await self._handle_delete(user, ai_intent)
        else:
            context_info = "I understood your intent as " + ai_intent.intent + " but I don't have a handler for it yet."

        # 3. Generate AI Response
        ai_response = await self.ai_service.generate_response(message, context_info)
        
        await self.db.commit()
        
        return ai_response, ai_intent.intent

    async def _handle_store(self, user: User, ai_intent: AIIntentResponse):
        obj_data = ai_intent.object
        loc_data = ai_intent.location
        
        if not obj_data or not loc_data:
            return "Missing object or location information."
        
        # Resolve hierarchical location
        location = await self._resolve_location(user.id, loc_data)
        
        # Check if object exists
        existing_obj = await self.repo.get_object_by_name(user.id, obj_data.name)
        if existing_obj:
            # Maybe move it? Or just update it?
            prev_loc_str = self._format_location(existing_obj.current_location)
            existing_obj.current_location_id = location.id
            new_loc_str = self._format_location(location)
            await self.repo.create_history(existing_obj.id, prev_loc_str, new_loc_str, "Stored again / updated location")
            return f"Updated location for {obj_data.name} to {new_loc_str}."
        
        # Create object
        obj = await self.repo.create_object(user.id, obj_data.name, obj_data.category, obj_data.description)
        obj.current_location_id = location.id
        
        new_loc_str = self._format_location(location)
        await self.repo.create_history(obj.id, "None", new_loc_str, "Initial storage")
        
        return f"Stored {obj.name} in {new_loc_str}."

    async def _handle_move(self, user: User, ai_intent: AIIntentResponse):
        obj_data = ai_intent.object
        loc_data = ai_intent.location
        
        if not obj_data or not loc_data:
            return "Missing object or destination location information."
            
        obj = await self.repo.get_object_by_name(user.id, obj_data.name)
        if not obj:
            return f"I couldn't find an object named {obj_data.name} to move. Should I store it for the first time?"
            
        location = await self._resolve_location(user.id, loc_data)
        
        prev_loc_str = self._format_location(obj.current_location)
        obj.current_location_id = location.id
        new_loc_str = self._format_location(location)
        
        await self.repo.create_history(obj.id, prev_loc_str, new_loc_str, "Moved by user request")
        
        return f"Moved {obj.name} from {prev_loc_str} to {new_loc_str}."

    async def _handle_find(self, user: User, ai_intent: AIIntentResponse):
        obj_data = ai_intent.object
        if not obj_data:
            return "I'm not sure which object you are looking for."
            
        obj = await self.repo.get_object_by_name(user.id, obj_data.name)
        if not obj:
            return f"I don't have any record of {obj_data.name}."
            
        loc_str = self._format_location(obj.current_location)
        return f"The {obj.name} is in {loc_str}."

    async def _handle_list(self, user: User, ai_intent: AIIntentResponse):
        loc_data = ai_intent.location
        if loc_data and loc_data.room:
            room = await self.repo.get_room_by_name(user.id, loc_data.room)
            if not room:
                return f"I don't see any record of a room called {loc_data.room}."
            
            all_objects = await self.repo.get_objects(user.id)
            room_objects = [o for o in all_objects if o.current_location and o.current_location.room_id == room.id]
            
            if not room_objects:
                return f"There are no objects recorded in the {room.name}."
            
            obj_list = ", ".join([o.name for o in room_objects])
            return f"Objects in the {room.name}: {obj_list}."
        else:
            objects = await self.repo.get_objects(user.id)
            if not objects:
                return "You haven't stored any objects yet."
            obj_list = ", ".join([f"{o.name} ({self._format_location(o.current_location)})" for o in objects])
            return f"You have the following objects: {obj_list}."

    async def _handle_delete(self, user: User, ai_intent: AIIntentResponse):
        obj_data = ai_intent.object
        if not obj_data:
            return "I'm not sure which object you want to delete."
        # Deletion logic usually requires repository support for actual delete or marking as inactive
        return "I understood you want to delete an object, but deletion is not fully implemented yet."

    async def _resolve_location(self, user_id: int, loc_data):
        room = await self.repo.get_room_by_name(user_id, loc_data.room)
        if not room:
            room = await self.repo.create_room(user_id, loc_data.room)
            
        furniture_id = None
        if loc_data.furniture:
            furniture = await self.repo.get_or_create_furniture(room.id, loc_data.furniture)
            furniture_id = furniture.id
            
        container_id = None
        if loc_data.container:
            if not furniture_id:
                # Fallback: create a generic furniture if container is specified without furniture
                furniture = await self.repo.get_or_create_furniture(room.id, "Generic Furniture")
                furniture_id = furniture.id
            container = await self.repo.get_or_create_container(furniture_id, loc_data.container)
            container_id = container.id
            
        return await self.repo.get_or_create_location(room.id, furniture_id, container_id)

    def _format_location(self, location: Location):
        if not location:
            return "Unknown"
        parts = [location.room.name]
        if location.furniture:
            parts.append(location.furniture.name)
        if location.container:
            parts.append(location.container.name)
        return " -> ".join(parts)
