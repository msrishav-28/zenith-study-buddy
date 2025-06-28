from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from app.database import Base

class SessionType(str, enum.Enum):
    TUTOR = "tutor"
    LANGUAGE_PRACTICE = "language_practice"
    EXAM_PREP = "exam_prep"
    PRONUNCIATION = "pronunciation"

class SessionStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class LearningSession(Base):
    __tablename__ = "learning_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    omnidim_session_id = Column(String, unique=True, nullable=False)
    
    # Session details
    type = Column(Enum(SessionType), nullable=False)
    status = Column(Enum(SessionStatus), default=SessionStatus.ACTIVE)
    subject = Column(String)
    language = Column(String)
    difficulty = Column(String)
    
    # Timing
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer, default=0)
    
    # Metrics
    interaction_count = Column(Integer, default=0)
    average_emotion_score = Column(Float)
    pronunciation_score = Column(Float)
    comprehension_score = Column(Float)
    
    # Configuration
    config = Column(JSON)
    
    # Relationships
    user = relationship("User", back_populates="learning_sessions")
    voice_interactions = relationship("VoiceInteraction", back_populates="session")