from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.progress import Progress, Achievement
from app.schemas.learning import ProgressResponse, AchievementResponse
from app.services.analytics.learning_insights import LearningInsightsService

router = APIRouter()
insights_service = LearningInsightsService()

@router.get("/", response_model=ProgressResponse)
async def get_user_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's overall progress"""
    progress = db.query(Progress).filter(
        Progress.user_id == current_user.id
    ).first()
    
    if not progress:
        # Create default progress entry
        progress = Progress(user_id=current_user.id)
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    return progress

@router.get("/achievements", response_model=List[AchievementResponse])
async def get_user_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's achievements"""
    achievements = db.query(Achievement).filter(
        Achievement.user_id == current_user.id
    ).order_by(Achievement.earned_at.desc()).all()
    
    return achievements

@router.post("/update-streak")
async def update_study_streak(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's study streak"""
    progress = db.query(Progress).filter(
        Progress.user_id == current_user.id
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    # Update streak logic
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    
    if progress.last_study_date:
        last_study = progress.last_study_date.date()
        days_diff = (today - last_study).days
        
        if days_diff == 1:
            # Continue streak
            progress.current_streak += 1
            if progress.current_streak > progress.longest_streak:
                progress.longest_streak = progress.current_streak
        elif days_diff > 1:
            # Break streak
            progress.current_streak = 1
    else:
        # First study session
        progress.current_streak = 1
        progress.longest_streak = 1
    
    progress.last_study_date = datetime.utcnow()
    db.commit()
    
    return {
        "current_streak": progress.current_streak,
        "longest_streak": progress.longest_streak
    }