import os
import json
from openai import AsyncOpenAI
from app.schemas.ai import AIIntentResponse, Intent
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are HomeMind, an AI memory assistant that remembers where physical objects are located inside a user's home.
Your job is to detect the user's intent and extract structured entities from their message.

Supported Intents:
- StoreObject: User wants to store a new object in a location.
- MoveObject: User moved an object to a new location.
- DeleteObject: User wants to forget/delete an object.
- FindObject: User asks where an object is.
- ListObjects: User asks what objects they have.
- ListRoom: User asks what is in a specific room.
- UpdateDescription: User wants to update the description or category of an object.
- Unknown: Any other intent.

Return the result as a structured JSON object.
"""

class AIService:
    async def detect_intent(self, message: str) -> AIIntentResponse:
        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message}
                ],
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            return AIIntentResponse(**data)
        except Exception as e:
            # Fallback for errors
            return AIIntentResponse(
                intent=Intent.UNKNOWN,
                entities={},
                confidence=0.0,
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
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are HomeMind, a helpful AI memory assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
