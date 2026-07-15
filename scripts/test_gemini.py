import asyncio
import os
import sys
from dotenv import load_dotenv

# Add backend to path so we can import app
sys.path.append(os.path.join(os.getcwd(), 'backend'))

load_dotenv()

from app.ai.providers.gemini_provider import GeminiProvider
from app.schemas.ai import AIIntentResponse

async def test_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("AI_MODEL", "gemini-3.5-flash")
    
    print(f"Testing Gemini with model: {model_name}")
    
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment")
        return

    provider = GeminiProvider(api_key=api_key, model_name=model_name)
    
    # Test simple completion
    print("\nTesting simple completion...")
    try:
        res = await provider.get_completion(
            prompt="Say 'Hello, Gemini is working!'",
            system_prompt="You are a helpful assistant."
        )
        print(f"Response: {res.get('content')}")
    except Exception as e:
        print(f"Simple completion failed: {e}")

    # Test structured completion
    print("\nTesting structured completion...")
    try:
        res = await provider.get_completion(
            prompt="Remember my passport is in the desk drawer in the office.",
            system_prompt="You are HomeMind AI. Extract the intent and details.",
            response_model=AIIntentResponse
        )
        print(f"Response: {res}")
    except Exception as e:
        print(f"Structured completion failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini())
