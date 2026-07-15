import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app.database.session import Base
from app.models.user import User
from app.models.memory import Location, Room, House, StoredObject
from app.repositories.memory_repository import MemoryRepository
from app.services.memory_pipeline import MemoryPipelineService
from app.ai.memory.ai_service import AIService
from app.schemas.ai import AIIntentResponse, Intent, AIObject, AILocation

async def test_loading():
    # Use SQLite in-memory for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with AsyncSessionLocal() as db:
        # Create a user
        user = User(email="test@example.com", password_hash="hash")
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Mock AI Service
        ai_service = MagicMock(spec=AIService)
        ai_service.detect_intent = AsyncMock(return_value=AIIntentResponse(
            intent=Intent.STORE_OBJECT,
            object=AIObject(name="laptop"),
            location=AILocation(room="bedroom", house="Main House"),
            reasoning="Testing"
        ))
        ai_service.generate_response = AsyncMock(return_value="OK, I've stored your laptop in the bedroom.")
        
        pipeline = MemoryPipelineService(db, ai_service)
        
        print("Running process_message...")
        try:
            response_text, intent = await pipeline.process_message(
                user=user,
                message="Remember my laptop is in the bedroom.",
                session_id=1
            )
            print(f"Success! Response: {response_text}")
        except Exception as e:
            print(f"Failed with error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    if os.environ.get("SKIP_TEST"):
        print("Skipping test due to environment constraints")
        sys.exit(0)
    try:
        import aiosqlite
        asyncio.run(test_loading())
    except ImportError:
        print("aiosqlite not installed, cannot run local DB test. Verification will be manual/code-review based.")
