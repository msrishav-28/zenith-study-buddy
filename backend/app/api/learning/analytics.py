from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.learning import AnalyticsResponse
from app.services.analytics.learning_insights import LearningInsightsService

router = APIRouter()
insights_service = LearningInsightsService()

@router.get("/dashboard", response_model=AnalyticsResponse)
async def get_analytics_dashboard(
    timeframe: str = Query("week", regex="^(week|month|year)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get analytics dashboard data"""
    analytics = await insights_service.generate_dashboard(
        user_id=current_user.id,
        timeframe=timeframe,
        db=db
    )
    return analytics

@router.get("/insights")
async def get_learning_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized learning insights"""
    insights = await insights_service.generate_insights(
        user_id=current_user.id,
        db=db
    )
    return {"insights": insights}

@router.get("/performance-trends")
async def get_performance_trends(
    metric: str = Query("accuracy", regex="^(accuracy|pronunciation|fluency|time)$"),
    days: int = Query(30, ge=7, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get performance trends over time"""
    trends = await insights_service.calculate_trends(
        user_id=current_user.id,
        metric=metric,
        days=days,
        db=db
    )
    return {"trends": trends}

@router.get("/recommendations")
async def get_study_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized study recommendations"""
    recommendations = await insights_service.generate_recommendations(
        user_id=current_user.id,
        db=db
    )
    return {"recommendations": recommendations}