from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.schemas.ai import ChatRequest, ChatResponse
from backend.app.services.memory_pipeline import MemoryPipelineService
from backend.app.ai.memory.ai_service import AIService
from backend.app.middleware.auth import get_current_user
from backend.app.models.user import User

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ai_service = AIService()
    pipeline = MemoryPipelineService(db, ai_service)
    
    # Session ID handling (simplified for now)
    session_id = request.session_id or 1
    
    response_text, intent = await pipeline.process_message(
        user=current_user,
        message=request.message,
        session_id=session_id
    )
    
    return ChatResponse(
        response=response_text,
        intent=intent,
        session_id=session_id
    )
