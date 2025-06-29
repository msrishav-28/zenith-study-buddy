from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.voice import VoiceSessionCreate, VoiceSessionResponse
from app.services.omnidim.voice_session import VoiceSessionManager

router = APIRouter()
session_manager = VoiceSessionManager()

@router.post("/start", response_model=VoiceSessionResponse)
async def start_exam_prep_session(
    exam_type: str,
    topics: List[str],
    question_count: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start an exam preparation session"""
    try:
        session = await session_manager.create_exam_prep_session(
            user_id=current_user.id,
            exam_type=exam_type,
            topics=topics,
            question_count=question_count
        )
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/exams")
async def get_available_exams():
    """Get list of available exam types"""
    return {
        "exams": [
            {
                "id": "sat",
                "name": "SAT",
                "subjects": ["math", "reading", "writing"]
            },
            {
                "id": "gre",
                "name": "GRE",
                "subjects": ["verbal", "quantitative", "analytical_writing"]
            },
            {
                "id": "toefl",
                "name": "TOEFL",
                "subjects": ["reading", "listening", "speaking", "writing"]
            },
            {
                "id": "ap_calculus",
                "name": "AP Calculus",
                "subjects": ["limits", "derivatives", "integrals", "series"]
            }
        ]
    }

@router.get("/topics/{exam_type}")
async def get_exam_topics(exam_type: str):
    """Get topics for a specific exam"""
    # In a real app, this would be from a database
    topics_map = {
        "sat": {
            "math": ["algebra", "geometry", "trigonometry", "statistics"],
            "reading": ["comprehension", "vocabulary", "analysis"],
            "writing": ["grammar", "essay", "rhetoric"]
        },
        "gre": {
            "verbal": ["vocabulary", "reading_comprehension", "text_completion"],
            "quantitative": ["arithmetic", "algebra", "geometry", "data_analysis"]
        }
    }
    
    if exam_type not in topics_map:
        raise HTTPException(status_code=404, detail="Exam type not found")
    
    return {"topics": topics_map[exam_type]}