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
async def start_language_practice(
    target_language: str,
    scenario: str,
    proficiency: str = "intermediate",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a language practice session"""
    try:
        session = await session_manager.create_language_practice_session(
            user_id=current_user.id,
            target_language=target_language,
            native_language=current_user.preferred_language,
            scenario=scenario,
            proficiency=proficiency
        )
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "languages": [
            {"code": "es", "name": "Spanish", "native_name": "Español"},
            {"code": "fr", "name": "French", "native_name": "Français"},
            {"code": "de", "name": "German", "native_name": "Deutsch"},
            {"code": "it", "name": "Italian", "native_name": "Italiano"},
            {"code": "pt", "name": "Portuguese", "native_name": "Português"},
            {"code": "zh", "name": "Chinese", "native_name": "中文"},
            {"code": "ja", "name": "Japanese", "native_name": "日本語"},
            {"code": "ko", "name": "Korean", "native_name": "한국어"}
        ]
    }

@router.get("/scenarios")
async def get_practice_scenarios():
    """Get available practice scenarios"""
    return {
        "scenarios": [
            {
                "id": "restaurant",
                "name": "Restaurant & Dining",
                "description": "Order food, ask about menu items",
                "difficulty": ["beginner", "intermediate", "advanced"]
            },
            {
                "id": "travel",
                "name": "Travel & Tourism",
                "description": "Airport, hotels, directions",
                "difficulty": ["beginner", "intermediate", "advanced"]
            },
            {
                "id": "business",
                "name": "Business Meeting",
                "description": "Professional conversations, presentations",
                "difficulty": ["intermediate", "advanced"]
            },
            {
                "id": "shopping",
                "name": "Shopping",
                "description": "Buy items, ask about prices",
                "difficulty": ["beginner", "intermediate"]
            },
            {
                "id": "medical",
                "name": "Medical Appointment",
                "description": "Describe symptoms, understand instructions",
                "difficulty": ["intermediate", "advanced"]
            }
        ]
    }