from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.voice import VoiceSessionCreate, VoiceSessionResponse
from app.services.omnidim.voice_session import VoiceSessionManager

router = APIRouter()

@router.post("/start", response_model=VoiceSessionResponse)
async def start_tutor_session(
    session_data: VoiceSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start an AI tutor voice session"""
    try:
        session_manager = VoiceSessionManager()
        
        # Create session with proper parameters
        session = await session_manager.create_tutor_session(
            user_id=current_user.id,
            subject=session_data.subject,
            difficulty=session_data.difficulty,
            learning_style=current_user.learning_style.value
        )
        
        return VoiceSessionResponse(
            session_id=session["session_id"],
            omnidim_session_id=session["session_id"],
            ws_endpoint=session["ws_endpoint"],
            voice_config=session["voice_config"],
            created_at=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))