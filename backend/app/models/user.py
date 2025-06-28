from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.database import Base

class LearningStyle(str, enum.Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING_WRITING = "reading_writing"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    
    # Learning preferences
    learning_style = Column(Enum(LearningStyle), default=LearningStyle.VISUAL)
    preferred_language = Column(String, default="en-US")
    preferred_voice_id = Column(String, default="tutor_friendly_sarah")
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    learning_sessions = relationship("LearningSession", back_populates="user")
    voice_interactions = relationship("VoiceInteraction", back_populates="user")
    progress = relationship("Progress", back_populates="user", uselist=False)
    achievements = relationship("Achievement", back_populates="user")