import os
import json
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from .base import AIProvider

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def get_completion(
        self, 
        prompt: str, 
        system_prompt: str, 
        response_model: Optional[Any] = None
    ) -> Dict[str, Any]:
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        if response_model:
            # Using new structured outputs API if possible, 
            # or just simple JSON mode if supported
            response = await self.client.beta.chat.completions.parse(
                model=self.model,
                messages=messages,
                response_format=response_model
            )
            return response.choices[0].message.parsed.model_dump()
        else:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return {"content": response.choices[0].message.content}
