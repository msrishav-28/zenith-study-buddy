from typing import Dict, Optional
import logging
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.learning_session import LearningSession
from app.models.voice_interaction import VoiceInteraction

logger = logging.getLogger(__name__)

class AdaptiveEngine:
    """Adapts learning content based on user performance"""
    
    def calculate_next_difficulty(
        self,
        current_difficulty: str,
        performance_score: float,
        user_history: list
    ) -> str:
        """Calculate appropriate difficulty for next content"""
        
        difficulty_levels = ["beginner", "elementary", "intermediate", "advanced", "expert"]
        current_index = difficulty_levels.index(current_difficulty)
        
        # Adjust based on performance
        if performance_score > 0.85 and current_index < len(difficulty_levels) - 1:
            # Move up
            return difficulty_levels[current_index + 1]
        elif performance_score < 0.60 and current_index > 0:
            # Move down
            return difficulty_levels[current_index - 1]
        
        return current_difficulty
    
    def get_adaptive_content(
        self,
        user: User,
        subject: str,
        current_performance: Dict,
        db: Session
    ) -> Dict:
        """Get content adapted to user's current level"""
        
        # Analyze recent performance
        recent_sessions = db.query(LearningSession).filter(
            LearningSession.user_id == user.id,
            LearningSession.subject == subject
        ).order_by(LearningSession.started_at.desc()).limit(5).all()
        
        avg_score = sum(s.comprehension_score or 0 for s in recent_sessions) / len(recent_sessions) if recent_sessions else 0.5
        
        # Determine content parameters
        content_params = {
            "difficulty": self.calculate_next_difficulty(
                current_performance.get("difficulty", "intermediate"),
                avg_score,
                recent_sessions
            ),
            "focus_areas": self._identify_weak_areas(recent_sessions),
            "preferred_style": user.learning_style,
            "pace": self._calculate_pace(current_performance)
        }
        
        return content_params
    
    def _identify_weak_areas(self, sessions: list) -> list:
        """Identify areas needing more focus"""
        # Analyze interaction patterns
        weak_areas = []
        
        # This would analyze actual interaction data
        # For now, return placeholder
        return ["pronunciation", "vocabulary"]
    
    def _calculate_pace(self, performance: Dict) -> str:
        """Calculate appropriate learning pace"""
        emotion = performance.get("emotion", "neutral")
        accuracy = performance.get("accuracy", 0.7)
        
        if emotion in ["frustrated", "confused"]:
            return "slower"
        elif emotion == "bored" and accuracy > 0.8:
            return "faster"
        
        return "normal"