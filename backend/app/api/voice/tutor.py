from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.voice import VoiceSessionCreate, VoiceSessionResponse
from app.services.omnidim.voice_session import VoiceSessionManager

router = APIRouter()
session_manager = VoiceSessionManager()

@router.post("/start", response_model=VoiceSessionResponse)
async def start_tutor_session(
    session_data: VoiceSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        session = session_manager.start_session(
            db=db,
            user=current_user,
            session_data=session_data
        )
        return session
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))