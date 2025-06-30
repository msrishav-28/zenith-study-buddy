from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base

class InteractionType(str, enum.Enum):
    USER_SPEECH = "user_speech"
    AI_RESPONSE = "ai_response"
    PRONUNCIATION_FEEDBACK = "pronunciation_feedback"
    EMOTION_DETECTION = "emotion_detection"
    LEARNING_INSIGHT = "learning_insight"

class VoiceInteraction(Base):
    __tablename__ = "voice_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("learning_sessions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Interaction details
    type = Column(Enum(InteractionType), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Content
    transcript = Column(Text)
    audio_url = Column(String)
    
    # Analysis results
    emotion = Column(String)
    emotion_confidence = Column(Float)
    pronunciation_score = Column(Float)
    fluency_score = Column(Float)
    
    # Metadata
    interaction_metadata = Column(JSON)
    
    # Relationships
    session = relationship("LearningSession", back_populates="voice_interactions")
    user = relationship("User", back_populates="voice_interactions")