import os
from typing import Optional
from backend.app.schemas.ai import AIIntentResponse, Intent
from backend.app.ai.providers.base import AIProvider
from backend.app.ai.providers.openai_provider import OpenAIProvider

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
            api_key = os.getenv("OPENAI_API_KEY")
            self.provider = OpenAIProvider(api_key=api_key)
        else:
            self.provider = provider

    async def detect_intent(self, message: str) -> AIIntentResponse:
        try:
            data = await self.provider.get_completion(
                prompt=message,
                system_prompt=SYSTEM_PROMPT,
                response_model=AIIntentResponse
            )
            return AIIntentResponse(**data)
        except Exception as e:
            # Fallback for errors
            return AIIntentResponse(
                intent=Intent.UNKNOWN,
                reasoning=str(e)
            )

    async def generate_response(self, message: str, context_info: str) -> str:
        prompt = f"""
        User Message: {message}
        Current Database Context: {context_info}
        
        Generate a helpful response to the user based ONLY on the provided context. 
        If the information is missing, ask a follow-up question.
        Never invent locations.
        """
        response = await self.provider.get_completion(
            prompt=prompt,
            system_prompt="You are HomeMind, a helpful AI memory assistant."
        )
        return response.get("content", "I encountered an error generating a response.")
