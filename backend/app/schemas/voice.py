from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.models.learning_session import SessionType
from app.models.voice_interaction import InteractionType

class VoiceSessionCreate(BaseModel):
    type: SessionType
    subject: Optional[str] = None
    language: Optional[str] = "en-US"
    difficulty: Optional[str] = "medium"
    config: Optional[Dict[str, Any]] = {}

class VoiceSessionResponse(BaseModel):
    session_id: str
    omnidim_session_id: str
    ws_endpoint: str
    voice_config: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True

class VoiceInteractionCreate(BaseModel):
    type: InteractionType
    transcript: Optional[str] = None
    emotion: Optional[str] = None
    emotion_confidence: Optional[float] = None
    pronunciation_score: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = {}

class PronunciationAnalysis(BaseModel):
    overall_score: float
    phoneme_scores: List[Dict[str, Any]]
    fluency_score: float
    suggestions: List[str]
    audio_feedback_url: Optional[str] = None

class EmotionDetection(BaseModel):
    primary_emotion: str
    confidence: float
    secondary_emotions: Optional[List[Dict[str, float]]] = []
    teaching_adaptation: Dict[str, Any]