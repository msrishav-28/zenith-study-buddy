from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.learning_session import LearningSession
from app.schemas.learning import LearningSessionResponse

router = APIRouter()

@router.get("/", response_model=List[LearningSessionResponse])
async def get_user_sessions(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's learning sessions"""
    query = db.query(LearningSession).filter(
        LearningSession.user_id == current_user.id
    )
    
    if session_type:
        query = query.filter(LearningSession.type == session_type)
    
    sessions = query.order_by(
        LearningSession.started_at.desc()
    ).offset(offset).limit(limit).all()
    
    return sessions

@router.get("/{session_id}", response_model=LearningSessionResponse)
async def get_session_details(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get details of a specific session"""
    session = db.query(LearningSession).filter(
        LearningSession.id == session_id,
        LearningSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session

@router.get("/recent/summary")
async def get_recent_sessions_summary(
    days: int = Query(7, ge=1, le=30),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get summary of recent sessions"""
    since_date = datetime.utcnow() - timedelta(days=days)
    
    sessions = db.query(LearningSession).filter(
        LearningSession.user_id == current_user.id,
        LearningSession.started_at >= since_date
    ).all()
    
    summary = {
        "total_sessions": len(sessions),
        "total_time": sum(s.duration_seconds for s in sessions),
        "by_type": {},
        "by_day": {},
        "average_duration": 0
    }
    
    if sessions:
        summary["average_duration"] = summary["total_time"] / len(sessions)
        
        # Group by type
        for session in sessions:
            if session.type not in summary["by_type"]:
                summary["by_type"][session.type] = 0
            summary["by_type"][session.type] += 1
            
            # Group by day
            day = session.started_at.date().isoformat()
            if day not in summary["by_day"]:
                summary["by_day"][day] = 0
            summary["by_day"][day] += 1
    
    return summary