from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.voice import PronunciationAnalysis
from app.services.omnidim.speech_analysis import SpeechAnalyzer

router = APIRouter()
speech_analyzer = SpeechAnalyzer()

@router.post("/analyze", response_model=PronunciationAnalysis)
async def analyze_pronunciation(
    audio_file: UploadFile = File(...),
    target_text: str = None,
    language: str = "en-US",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze pronunciation of uploaded audio"""
    try:
        audio_data = await audio_file.read()
        
        analysis = await speech_analyzer.analyze_pronunciation(
            audio_data=audio_data,
            target_text=target_text,
            language=language,
            user_id=current_user.id
        )
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/practice/{word}")
async def practice_word_pronunciation(
    word: str,
    language: str = "en-US",
    current_user: User = Depends(get_current_user)
):
    """Get pronunciation guide for a specific word"""
    try:
        guide = await speech_analyzer.get_pronunciation_guide(word, language)
        return guide
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/common-mistakes/{language}")
async def get_common_pronunciation_mistakes(
    language: str,
    native_language: str = None,
    current_user: User = Depends(get_current_user)
):
    """Get common pronunciation mistakes for language learners"""
    mistakes = await speech_analyzer.get_common_mistakes(
        target_language=language,
        native_language=native_language or current_user.preferred_language
    )
    return {"mistakes": mistakes}