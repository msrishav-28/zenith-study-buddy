from typing import Dict, List
from datetime import datetime, timedelta
import logging

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.models.learning_session import LearningSession
from app.models.progress import Progress

logger = logging.getLogger(__name__)

class LearningInsightsService:
    """Generates personalized learning insights"""
    
    async def generate_dashboard(
        self,
        user_id: int,
        timeframe: str,
        db: Session
    ) -> Dict:
        """Generate analytics dashboard data"""
        
        # Calculate date range
        if timeframe == "week":
            since_date = datetime.utcnow() - timedelta(days=7)
        elif timeframe == "month":
            since_date = datetime.utcnow() - timedelta(days=30)
        else:  # year
            since_date = datetime.utcnow() - timedelta(days=365)
        
        # Get sessions
        sessions = db.query(LearningSession).filter(
            LearningSession.user_id == user_id,
            LearningSession.started_at >= since_date
        ).all()
        
        # Calculate daily stats
        daily_stats = self._calculate_daily_stats(sessions)
        
        # Get progress
        progress = db.query(Progress).filter(Progress.user_id == user_id).first()
        
        return {
            "daily_stats": daily_stats,
            "weekly_progress": self._calculate_weekly_progress(sessions),
            "learning_insights": await self.generate_insights(user_id, db),
            "recommended_focus_areas": self._get_recommendations(sessions, progress)
        }
    
    async def generate_insights(
        self,
        user_id: int,
        db: Session
    ) -> List[str]:
        """Generate personalized learning insights"""
        
        insights = []
        
        # Get recent sessions
        recent_sessions = db.query(LearningSession).filter(
            LearningSession.user_id == user_id
        ).order_by(LearningSession.started_at.desc()).limit(10).all()
        
        if not recent_sessions:
            return ["Start your first learning session to get personalized insights!"]
        
        # Analyze patterns
        avg_duration = sum(s.duration_seconds for s in recent_sessions) / len(recent_sessions)
        if avg_duration < 600:  # Less than 10 minutes
            insights.append("Try longer study sessions (15-20 minutes) for better retention")
        elif avg_duration > 3600:  # More than 1 hour
            insights.append("Consider taking breaks every 25-30 minutes to maintain focus")
        
        # Check consistency
        unique_days = len(set(s.started_at.date() for s in recent_sessions))
        if unique_days >= 7:
            insights.append("Excellent consistency! You've studied every day this week")
        elif unique_days < 3:
            insights.append("Try to study more consistently - aim for at least 4 days per week")
        
        # Performance trends
        if len(recent_sessions) >= 3:
            recent_scores = [s.comprehension_score for s in recent_sessions[:3] if s.comprehension_score]
            if recent_scores and sum(recent_scores) / len(recent_scores) > 0.8:
                insights.append("Great progress! Consider moving to more advanced topics")
        
        return insights
    
    async def calculate_trends(
        self,
        user_id: int,
        metric: str,
        days: int,
        db: Session
    ) -> List[Dict]:
        """Calculate performance trends"""
        
        since_date = datetime.utcnow() - timedelta(days=days)
        sessions = db.query(LearningSession).filter(
            LearningSession.user_id == user_id,
            LearningSession.started_at >= since_date
        ).all()
        
        # Group by day
        daily_data = {}
        for session in sessions:
            day = session.started_at.date().isoformat()
            if day not in daily_data:
                daily_data[day] = []
            daily_data[day].append(session)
        
        # Calculate metric for each day
        trends = []
        for day, day_sessions in sorted(daily_data.items()):
            if metric == "accuracy":
                value = sum(s.comprehension_score or 0 for s in day_sessions) / len(day_sessions)
            elif metric == "pronunciation":
                value = sum(s.pronunciation_score or 0 for s in day_sessions) / len(day_sessions)
            elif metric == "time":
                value = sum(s.duration_seconds for s in day_sessions) / 60  # minutes
            else:
                value = 0
            
            trends.append({
                "date": day,
                "value": round(value, 2)
            })
        
        return trends
    
    async def generate_recommendations(
        self,
        user_id: int,
        db: Session
    ) -> List[Dict]:
        """Generate personalized study recommendations"""
        
        recommendations = []
        
        # Get user's weak areas
        recent_sessions = db.query(LearningSession).filter(
            LearningSession.user_id == user_id
        ).order_by(LearningSession.started_at.desc()).limit(20).all()
        
        # Analyze performance by subject
        subject_performance = {}
        for session in recent_sessions:
            if session.subject:
                if session.subject not in subject_performance:
                    subject_performance[session.subject] = []
                if session.comprehension_score:
                    subject_performance[session.subject].append(session.comprehension_score)
        
        # Find weak subjects
        for subject, scores in subject_performance.items():
            avg_score = sum(scores) / len(scores) if scores else 0
            if avg_score < 0.7:
                recommendations.append({
                    "type": "focus_area",
                    "subject": subject,
                    "reason": "Below target performance",
                    "action": f"Spend more time on {subject} fundamentals"
                })
        
        # Check for variety
        unique_subjects = len(subject_performance.keys())
        if unique_subjects < 3:
            recommendations.append({
                "type": "variety",
                "reason": "Limited subject diversity",
                "action": "Try exploring new subjects to broaden your knowledge"
            })
        
        return recommendations
    
    def _calculate_daily_stats(self, sessions: List) -> List[Dict]:
        """Calculate daily statistics"""
        daily_stats = {}
        
        for session in sessions:
            day = session.started_at.date().isoformat()
            if day not in daily_stats:
                daily_stats[day] = {
                    "date": day,
                    "sessions": 0,
                    "total_time": 0,
                    "avg_score": 0,
                    "scores": []
                }
            
            daily_stats[day]["sessions"] += 1
            daily_stats[day]["total_time"] += session.duration_seconds    async def get_voice_models(self, language: Optional[str] = None) -> list:
        """Get available voice models"""
        params = {"language": language} if language else {}
        response = await self._client.get(
            f"{self.base_url}/voices",
            params=params
        )
        response.raise_for_status()
        return response.json()["voices"]
    
    async def close(self):
        """Close the HTTP client"""
        await self._client.aclose()