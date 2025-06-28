from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.models.learning_session import SessionType, SessionStatus

class LearningSessionResponse(BaseModel):
    id: str
    type: SessionType
    status: SessionStatus
    subject: Optional[str]
    started_at: datetime
    ended_at: Optional[datetime]
    duration_seconds: int
    interaction_count: int
    average_emotion_score: Optional[float]
    pronunciation_score: Optional[float]
    
    class Config:
        from_attributes = True

class ProgressResponse(BaseModel):
    total_study_time: int
    total_sessions: int
    current_streak: int
    longest_streak: int
    level: int
    experience_points: int
    overall_accuracy: float
    subject_progress: Dict[str, Any]
    
    class Config:
        from_attributes = True

class AchievementResponse(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    category: str
    earned_at: datetime
    progress_value: int
    progress_max: int
    
    class Config:
        from_attributes = True

class AnalyticsResponse(BaseModel):
    daily_stats: List[Dict[str, Any]]
    weekly_progress: Dict[str, Any]
    learning_insights: List[str]
    recommended_focus_areas: List[str]