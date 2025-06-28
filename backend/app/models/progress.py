from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Overall stats
    total_study_time = Column(Integer, default=0)  # seconds
    total_sessions = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_study_date = Column(DateTime(timezone=True))
    
    # Performance metrics
    overall_accuracy = Column(Float, default=0.0)
    pronunciation_average = Column(Float, default=0.0)
    fluency_average = Column(Float, default=0.0)
    
    # Subject progress
    subject_progress = Column(JSON, default={})
    
    # Level/XP system
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="progress")

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Achievement details
    name = Column(String, nullable=False)
    description = Column(String)
    icon = Column(String)
    category = Column(String)
    
    # Progress
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    progress_value = Column(Integer, default=0)
    progress_max = Column(Integer, default=100)
    
    # Relationships
    user = relationship("User", back_populates="achievements")

class StudyStreak(Base):
    __tablename__ = "study_streaks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Streak data
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True))
    days = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    
    # Freeze protection
    freeze_used = Column(Boolean, default=False)
    freeze_date = Column(DateTime(timezone=True))