import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional
from google import genai
from google.genai import types
from .base import AIProvider

logger = logging.getLogger(__name__)

class GeminiProvider(AIProvider):
    def __init__(self, api_key: str, model_name: str = "gemini-3.5-flash"):
        if not api_key:
            logger.error("GEMINI_API_KEY is missing")
            raise ValueError("GEMINI_API_KEY is not configured")

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        logger.info(f"GeminiProvider initialized with model: {self.model_name}")

    async def get_completion(
        self,
        prompt: str,
        system_prompt: str,
        response_model: Optional[Any] = None
    ) -> Dict[str, Any]:
        logger.info(f"Using Gemini Provider: {self.model_name}")

        config = {}
        if response_model:
            logger.info(f"Requesting structured output from Gemini for model {self.model_name}")
            config = {
                'response_mime_type': 'application/json',
                'response_schema': response_model,
                'system_instruction': system_prompt
            }
        else:
            config = {
                'system_instruction': system_prompt
            }

        try:
            # google-genai SDK 0.x models are mostly synchronous in the current version
            # or use a different client for async. 
            # To keep it simple and safe within the current architecture:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(**config)
                )
            )

            if response_model:
                try:
                    parsed_data = json.loads(response.text)
                    logger.debug(f"Gemini parsed output: {parsed_data}")
                    return parsed_data
                except Exception as e:
                    logger.error(f"Failed to parse Gemini JSON output: {e}. Raw: {response.text}")
                    raise ValueError(f"AI returned invalid structured data: {str(e)}")
            else:
                return {"content": response.text}

        except Exception as e:
            logger.error(f"Error calling Gemini API ({self.model_name}): {e}", exc_info=True)
            raise
