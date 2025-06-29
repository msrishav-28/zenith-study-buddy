from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import math
import logging

from sqlalchemy.orm import Session
from app.models.user import User

logger = logging.getLogger(__name__)

class SpacedRepetitionEngine:
    """Implements spaced repetition algorithm for optimal retention"""
    
    def calculate_next_review(
        self,
        quality: int,  # 0-5 (0=complete fail, 5=perfect)
        repetitions: int,
        ease_factor: float,
        interval: int
    ) -> Tuple[int, float, int]:
        """
        Calculate next review date using SM-2 algorithm
        Returns: (interval_days, new_ease_factor, new_repetitions)
        """
        
        if quality >= 3:
            if repetitions == 0:
                interval = 1
            elif repetitions == 1:
                interval = 6
            else:
                interval = math.ceil(interval * ease_factor)
            
            repetitions += 1
        else:
            repetitions = 0
            interval = 1
        
        # Update ease factor
        ease_factor = max(1.3, ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        
        return interval, ease_factor, repetitions
    
    def get_items_for_review(
        self,
        user_id: int,
        subject: str,
        db: Session,
        limit: int = 20
    ) -> List[Dict]:
        """Get items due for review"""
        
        # This would query actual review items from database
        # For now, return sample items
        items = []
        
        for i in range(min(5, limit)):
            items.append({
                "id": f"item_{i}",
                "content": f"Review item {i} for {subject}",
                "last_reviewed": datetime.utcnow() - timedelta(days=i),
                "ease_factor": 2.5,
                "interval": i + 1,
                "repetitions": i
            })
        
        return items
    
    def schedule_review(
        self,
        item_id: str,
        quality: int,
        user_id: int,
        db: Session
    ) -> Dict:
        """Schedule next review for an item"""
        
        # Get current item data (would be from database)
        current_interval = 1
        current_ease = 2.5
        current_reps = 0
        
        # Calculate next review
        new_interval, new_ease, new_reps = self.calculate_next_review(
            quality,
            current_reps,
            current_ease,
            current_interval
        )
        
        next_review_date = datetime.utcnow() + timedelta(days=new_interval)
        
        # Save to database (placeholder)
        
        return {
            "item_id": item_id,
            "next_review": next_review_date,
            "interval_days": new_interval,
            "ease_factor": new_ease,
            "repetitions": new_reps
        }
    
    def get_retention_stats(
        self,
        user_id: int,
        subject: str,
        db: Session
    ) -> Dict:
        """Get retention statistics for user"""
        
        # This would calculate from actual review history
        return {
            "average_retention": 0.85,
            "items_mastered": 42,
            "items_learning": 18,
            "items_difficult": 5,
            "streak_days": 7
        }