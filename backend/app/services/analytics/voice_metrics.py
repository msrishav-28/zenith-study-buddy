from typing import Dict, List
from datetime import datetime, timedelta
import logging

from sqlalchemy.orm import Session
from app.models.voice_interaction import VoiceInteraction

logger = logging.getLogger(__name__)

class VoiceMetricsAnalyzer:
    """Analyzes voice interaction metrics"""
    
    def calculate_speaking_metrics(
        self,
        user_id: int,
        session_id: str,
        db: Session
    ) -> Dict:
        """Calculate speaking performance metrics"""
        
        interactions = db.query(VoiceInteraction).filter(
            VoiceInteraction.user_id == user_id,
            VoiceInteraction.session_id == session_id
        ).all()
        
        if not interactions:
            return {}
        
        # Calculate metrics
        total_speaking_time = len([i for i in interactions if i.type == "user_speech"])
        avg_pronunciation = sum(i.pronunciation_score or 0 for i in interactions) / len(interactions)
        avg_fluency = sum(i.fluency_score or 0 for i in interactions) / len(interactions)
        
        emotions = [i.emotion for i in interactions if i.emotion]
        emotion_distribution = {}
        for emotion in emotions:
            emotion_distribution[emotion] = emotion_distribution.get(emotion, 0) + 1
        
        return {
            "total_interactions": len(interactions),
            "speaking_time_seconds": total_speaking_time * 3,  # Rough estimate
            "average_pronunciation_score": round(avg_pronunciation, 2),
            "average_fluency_score": round(avg_fluency, 2),
            "emotion_distribution": emotion_distribution,
            "improvement_areas": self._identify_improvement_areas(interactions)
        }
    
    def get_voice_trends(
        self,
        user_id: int,
        days: int,
        db: Session
    ) -> List[Dict]:
        """Get voice performance trends over time"""
        
        since_date = datetime.utcnow() - timedelta(days=days)
        
        # This would aggregate actual data
        # For now, return sample trend data
        trends = []
        for i in range(days):
            date = since_date + timedelta(days=i)
            trends.append({
                "date": date.isoformat(),
                "pronunciation_score": 0.7 + (i * 0.01),
                "fluency_score": 0.65 + (i * 0.015),
                "confidence_score": 0.6 + (i * 0.02),
                "sessions": 1 if i % 2 == 0 else 0
            })
        
        return trends
    
    def _identify_improvement_areas(self, interactions: List) -> List[str]:
        """Identify areas needing improvement"""
        areas = []
        
        avg_pronunciation = sum(i.pronunciation_score or 0 for i in interactions) / len(interactions)
        if avg_pronunciation < 0.7:
            areas.append("pronunciation")
        
        avg_fluency = sum(i.fluency_score or 0 for i in interactions) / len(interactions)
        if avg_fluency < 0.7:
            areas.append("fluency")
        
        # Check for frequent negative emotions
        negative_emotions = ["frustrated", "confused", "anxious"]
        emotion_count = sum(1 for i in interactions if i.emotion in negative_emotions)
        if emotion_count > len(interactions) * 0.3:
            areas.append("confidence")
        
        return areas