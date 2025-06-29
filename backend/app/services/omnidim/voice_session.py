### `backend/app/services/omnidim/voice_session.py`
```python
from typing import Dict, Optional, Any
import asyncio
import uuid
from datetime import datetime

from app.services.omnidim.client import OmnidimClient
from app.models.voice_interaction import VoiceInteraction
from app.models.learning_session import LearningSession, SessionType, SessionStatus
from app.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

class VoiceSessionManager:
    """Manages voice learning sessions with Omnidim"""
    
    def __init__(self):
        self.client = OmnidimClient()
        self.active_sessions: Dict[str, Dict] = {}
    
    async def create_tutor_session(
        self,
        user_id: int,
        subject: str,
        difficulty: str,
        learning_style: str
    ) -> Dict[str, Any]:
        """Create an AI tutor voice session"""
        
        session_config = {
            "mode": "tutor",
            "user_id": str(user_id),
            "context": {
                "subject": subject,
                "difficulty": difficulty,
                "learning_style": learning_style,
                "personality": self._get_tutor_personality(subject, learning_style)
            },
            "features": [
                "real_time_transcription",
                "emotion_detection",
                "adaptive_responses",
                "pronunciation_feedback",
                "interrupt_handling"
            ],
            "voice_id": self._select_voice_for_subject(subject),
            "language": "en-US"
        }
        
        # Create session with Omnidim
        omnidim_session = await self.client.create_voice_session(session_config)
        
        # Store session in database
        db = SessionLocal()
        try:
            db_session = LearningSession(
                id=str(uuid.uuid4()),
                user_id=user_id,
                omnidim_session_id=omnidim_session["session_id"],
                type=SessionType.TUTOR,
                subject=subject,
                difficulty=difficulty,
                config=session_config
            )
            db.add(db_session)
            db.commit()
            
            # Track active session
            self.active_sessions[omnidim_session["session_id"]] = {
                "user_id": user_id,
                "db_session_id": db_session.id,
                "started_at": datetime.utcnow()
            }
        finally:
            db.close()
        
        return {
            "session_id": omnidim_session["session_id"],
            "ws_endpoint": f"/api/ws/voice/{omnidim_session['session_id']}",
            "voice_config": {
                "voice_id": session_config["voice_id"],
                "personality": session_config["context"]["personality"]
            }
        }
    
    async def create_language_practice_session(
        self,
        user_id: int,
        target_language: str,
        native_language: str,
        scenario: str,
        proficiency: str
    ) -> Dict[str, Any]:
        """Create a language practice session"""
        
        session_config = {
            "mode": "language_practice",
            "user_id": str(user_id),
            "context": {
                "target_language": target_language,
                "native_language": native_language,
                "scenario": scenario,
                "proficiency": proficiency,
                "correction_style": "supportive"
            },
            "features": [
                "real_time_transcription",
                "pronunciation_scoring",
                "grammar_correction",
                "vocabulary_suggestions",
                "cultural_context"
            ],
            "voice_id": f"native_{target_language}",
            "language": target_language
        }
        
        omnidim_session = await self.client.create_voice_session(session_config)
        
        # Store in database
        db = SessionLocal()
        try:
            db_session = LearningSession(
                id=str(uuid.uuid4()),
                user_id=user_id,
                omnidim_session_id=omnidim_session["session_id"],
                type=SessionType.LANGUAGE_PRACTICE,
                language=target_language,
                config=session_config
            )
            db.add(db_session)
            db.commit()
        finally:
            db.close()
        
        return {
            "session_id": omnidim_session["session_id"],
            "ws_endpoint": f"/api/ws/voice/{omnidim_session['session_id']}",
            "scenario_context": self._get_scenario_context(scenario, target_language)
        }
    
    async def end_session(self, session_id: str, user_id: int):
        """End a voice session"""
        if session_id in self.active_sessions:
            session_info = self.active_sessions[session_id]
            
            # Update database
            db = SessionLocal()
            try:
                db_session = db.query(LearningSession).filter(
                    LearningSession.omnidim_session_id == session_id,
                    LearningSession.user_id == user_id
                ).first()
                
                if db_session:
                    db_session.status = SessionStatus.COMPLETED
                    db_session.ended_at = datetime.utcnow()
                    db_session.duration_seconds = int(
                        (db_session.ended_at - db_session.started_at).total_seconds()
                    )
                    db.commit()
            finally:
                db.close()
            
            # Remove from active sessions
            del self.active_sessions[session_id]
    
    def _get_tutor_personality(self, subject: str, learning_style: str) -> Dict:
        """Define tutor personality based on subject and learning style"""
        personalities = {
            "math": {
                "visual": {
                    "tone": "analytical",
                    "pace": "moderate",
                    "examples": "geometric",
                    "encouragement": "logical"
                },
                "auditory": {### `backend/app/api/voice/tutor.py`
```python
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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a voice tutoring session"""
    try:
        session = await session_manager.create_tutor_session(
            user_id=current_user.id,
            subject=session_data.subject,
            difficulty=session_data.difficulty,
            learning_style=current_user.learning_style
        )
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/end/{session_id}")
async def end_tutor_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """End a voice tutoring session"""
    await session_manager.end_session(session_id, current_user.id)
    return {"message": "Session ended successfully"}

@router.get("/subjects")
async def get_available_subjects():
    """Get list of available subjects for tutoring"""
    return {
        "subjects": [
            {"id": "math", "name": "Mathematics", "icon": "calculator"},
            {"id": "science", "name": "Science", "icon": "flask"},
            {"id": "language", "name": "Language Arts", "icon": "book"},
            {"id": "history", "name": "History", "icon": "clock"},
            {"id": "programming", "name": "Programming", "icon": "code"}
        ]
    }