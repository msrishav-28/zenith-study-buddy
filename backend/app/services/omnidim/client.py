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
