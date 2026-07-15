import os
import logging
from typing import Optional
from app.schemas.ai import AIIntentResponse, Intent
from app.ai.providers.base import AIProvider
from app.ai.providers.gemini_provider import GeminiProvider

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are HomeMind, an AI memory assistant that remembers where physical objects are located inside a user's home.
Your job is to detect the user's intent and extract structured entities from their message.

Supported Intents:
- STORE_OBJECT: User wants to store a new object in a location. Example: "Remember my screwdriver is in the garage."
- MOVE_OBJECT: User moved an object to a new location. Example: "I moved my passport to my office."
- FIND_OBJECT: User asks where an object is. Example: "Where is my passport?"
- LIST_OBJECTS: User asks what objects they have or what is in a specific room. Example: "What items are in my garage?"
- DELETE_OBJECT: User wants to forget/delete an object.
- UPDATE_OBJECT: User wants to update the description or category of an object.
- UNKNOWN: Any other intent.

Always return the response in the structured format provided.
"""

class AIService:
    def __init__(self, provider: Optional[AIProvider] = None):
        if provider is None:
            api_key = os.getenv("GEMINI_API_KEY")
            model_name = os.getenv("AI_MODEL", "gemini-3.5-flash")
            logger.info(f"Initializing AIService with GeminiProvider ({model_name})")
            try:
                self.provider = GeminiProvider(api_key=api_key, model_name=model_name)
            except ValueError as e:
                logger.error(f"Failed to initialize AI Provider: {e}")
                self.provider = None
        else:
            self.provider = provider

    async def detect_intent(self, message: str) -> AIIntentResponse:
        logger.info(f"Detecting intent for message: {message}")
        if not self.provider:
            return AIIntentResponse(
                intent=Intent.UNKNOWN,
                reasoning="AI Provider not initialized (check API key)"
            )
        try:
            data = await self.provider.get_completion(
                prompt=message,
                system_prompt=SYSTEM_PROMPT,
                response_model=AIIntentResponse
            )
            intent_res = AIIntentResponse(**data)
            logger.info(f"Extracted Intent: {intent_res.intent}")
            return intent_res
        except Exception as e:
            logger.error(f"Error detecting intent: {e}", exc_info=True)
            return AIIntentResponse(
                intent=Intent.UNKNOWN,
                reasoning=str(e)
            )

    async def generate_response(self, message: str, context_info: str) -> str:
        logger.info(f"Generating natural language response. Context: {context_info}")
        if not self.provider:
            return "AI service is currently unavailable. Please check the backend configuration."
        
        prompt = f"""
        User Message: {message}
        Current Database Context: {context_info}
        
        Generate a helpful, concise response to the user based ONLY on the provided context. 
        If information is being stored or moved, confirm it accurately.
        If information is missing, ask a follow-up question.
        Never invent locations.
        """
        try:
            response = await self.provider.get_completion(
                prompt=prompt,
                system_prompt="You are HomeMind, a helpful AI memory assistant."
            )
            return response.get("content", "I encountered an error generating a response.")
        except Exception as e:
            logger.error(f"Error generating response: {e}", exc_info=True)
            return f"Error: {str(e)}"
