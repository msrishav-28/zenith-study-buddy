from typing import Dict, Optional, Any
import asyncio
import uuid
from datetime import datetime

from app.services.omnidim.client import OmnidimClient
from app.models.voice_interaction import VoiceInteraction
from app.models.learning_session import LearningSession, SessionType, SessionStatus
from app.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

class VoiceSessionManager:
    """Manages voice learning sessions with Omnidim"""
    
    def __init__(self):
        self.client = OmnidimClient()
        self.active_sessions: Dict[str, Dict] = {}
    
    async def create_tutor_session(
        self,
        user_id: int,
        subject: str,
        difficulty: str,
        learning_style: str
    ) -> Dict[str, Any]:
        """Create an AI tutor voice session"""
        
        session_config = {
            "mode": "tutor",
            "user_id": str(user_id),
            "context": {
                "subject": subject,
                "difficulty": difficulty,
                "learning_style": learning_style,
                "personality": self._get_tutor_personality(subject, learning_style)
            },
            "features": [
                "real_time_transcription",
                "emotion_detection",
                "adaptive_responses",
                "pronunciation_feedback",
                "interrupt_handling"
            ],
            "voice_id": self._select_voice_for_subject(subject),
            "language": "en-US"
        }
        
        # Create session with Omnidim
        omnidim_session = await self.client.create_voice_session(session_config)
        
        # Store session in database
        db = SessionLocal()
        try:
            db_session = LearningSession(
                id=str(uuid.uuid4()),
                user_id=user_id,
                omnidim_session_id=omnidim_session["session_id"],
                type=SessionType.TUTOR,
                subject=subject,
                difficulty=difficulty,
                config=session_config
            )
            db.add(db_session)
            db.commit()
            
            # Track active session
            self.active_sessions[omnidim_session["session_id"]] = {
                "user_id": user_id,
                "db_session_id": db_session.id,
                "started_at": datetime.utcnow()
            }
        finally:
            db.close()
        
        return {
            "session_id": omnidim_session["session_id"],
            "ws_endpoint": f"/api/ws/voice/{omnidim_session['session_id']}",
            "voice_config": {
                "voice_id": session_config["voice_id"],
                "personality": session_config["context"]["personality"]
            }
        }
    
    async def create_language_practice_session(
        self,
        user_id: int,
        target_language: str,
        native_language: str,
        scenario: str,
        proficiency: str
    ) -> Dict[str, Any]:
        """Create a language practice session"""
        
        session_config = {
            "mode": "language_practice",
            "user_id": str(user_id),
            "context": {
                "target_language": target_language,
                "native_language": native_language,
                "scenario": scenario,
                "proficiency": proficiency,
                "correction_style": "supportive"
            },
            "features": [
                "real_time_transcription",
                "pronunciation_scoring",
                "grammar_correction",
                "vocabulary_suggestions",
                "cultural_context"
            ],
            "voice_id": f"native_{target_language}",
            "language": target_language
        }
        
        omnidim_session = await self.client.create_voice_session(session_config)
        
        # Store in database
        db = SessionLocal()
        try:
            db_session = LearningSession(
                id=str(uuid.uuid4()),
                user_id=user_id,
                omnidim_session_id=omnidim_session["session_id"],
                type=SessionType.LANGUAGE_PRACTICE,
                language=target_language,
                config=session_config
            )
            db.add(db_session)
            db.commit()
        finally:
            db.close()
        
        return {
            "session_id": omnidim_session["session_id"],
            "ws_endpoint": f"/api/ws/voice/{omnidim_session['session_id']}",
            "scenario_context": self._get_scenario_context(scenario, target_language)
        }

    async def create_exam_prep_session(
        self,
        user_id: int,
        exam_type: str,
        topics: List[str],
        question_count: int
    ) -> Dict[str, Any]:
        """Create an exam preparation session"""
        
        session_config = {
            "mode": "exam_prep",
            "user_id": str(user_id),
            "context": {
                "exam_type": exam_type,
                "topics": topics,
                "question_count": question_count,
                "adaptive_difficulty": True
            },
            "features": [
                "real_time_transcription",
                "answer_evaluation",
                "hint_system",
                "progress_tracking",
                "time_management"
            ],
            "voice_id": "tutor_professional",
            "language": "en-US"
        }
        
        omnidim_session = await self.client.create_voice_session(session_config)
        
        # Store in database
        db = SessionLocal()
        try:
            db_session = LearningSession(
                id=str(uuid.uuid4()),
                user_id=user_id,
                omnidim_session_id=omnidim_session["session_id"],
                type=SessionType.EXAM_PREP,
                config=session_config
            )
            db.add(db_session)
            db.commit()
        finally:
            db.close()
        
        return {
            "session_id": omnidim_session["session_id"],
            "ws_endpoint": f"/api/ws/voice/{omnidim_session['session_id']}",
            "exam_config": {
                "type": exam_type,
                "topics": topics,
                "questions": question_count
            }
        }
    
    async def pause_session(self, session_id: str, user_id: int):
        """Pause an active voice session"""
        if session_id in self.active_sessions:
            session_info = self.active_sessions[session_id]
            if session_info["user_id"] == user_id:
                # Call Omnidim to pause the session
                await self.client.pause_voice_session(session_id)
                
                # Update session status
                db = SessionLocal()
                try:
                    db_session = db.query(LearningSession).filter(
                        LearningSession.omnidim_session_id == session_id,
                        LearningSession.user_id == user_id
                    ).first()
                    
                    if db_session:
                        db_session.status = SessionStatus.PAUSED
                        db.commit()
                finally:
                    db.close()
    
    async def resume_session(self, session_id: str, user_id: int):
        """Resume a paused voice session"""
        if session_id in self.active_sessions:
            session_info = self.active_sessions[session_id]
            if session_info["user_id"] == user_id:
                # Call Omnidim to resume the session
                await self.client.resume_voice_session(session_id)
                
                # Update session status
                db = SessionLocal()
                try:
                    db_session = db.query(LearningSession).filter(
                        LearningSession.omnidim_session_id == session_id,
                        LearningSession.user_id == user_id
                    ).first()
                    
                    if db_session:
                        db_session.status = SessionStatus.ACTIVE
                        db.commit()
                finally:
                    db.close()
    
    async def end_session(self, session_id: str, user_id: int):
        """End a voice session"""
        if session_id in self.active_sessions:
            session_info = self.active_sessions[session_id]
            
            # End session with Omnidim
            await self.client.end_voice_session(session_id)
            
            # Update database
            db = SessionLocal()
            try:
                db_session = db.query(LearningSession).filter(
                    LearningSession.omnidim_session_id == session_id,
                    LearningSession.user_id == user_id
                ).first()
                
                if db_session:
                    db_session.status = SessionStatus.COMPLETED
                    db_session.ended_at = datetime.utcnow()
                    db_session.duration_seconds = int(
                        (db_session.ended_at - db_session.started_at).total_seconds()
                    )
                    db.commit()
            finally:
                db.close()
            
            # Remove from active sessions
            del self.active_sessions[session_id]
    
    async def get_session_status(self, session_id: str, user_id: int) -> Dict[str, Any]:
        """Get current session status"""
        if session_id not in self.active_sessions:
            return {"status": "not_found"}
        
        session_info = self.active_sessions[session_id]
        if session_info["user_id"] != user_id:
            return {"status": "unauthorized"}
        
        # Get status from Omnidim
        omnidim_status = await self.client.get_session_status(session_id)
        
        # Get database info
        db = SessionLocal()
        try:
            db_session = db.query(LearningSession).filter(
                LearningSession.omnidim_session_id == session_id,
                LearningSession.user_id == user_id
            ).first()
            
            if not db_session:
                return {"status": "not_found"}
            
            duration = (datetime.utcnow() - db_session.started_at).total_seconds()
            
            return {
                "status": "active",
                "session_id": session_id,
                "type": db_session.type.value,
                "duration_seconds": int(duration),
                "omnidim_status": omnidim_status,
                "started_at": db_session.started_at.isoformat()
            }
        finally:
            db.close()
    
    def _get_tutor_personality(self, subject: str, learning_style: str) -> Dict:
        """Define tutor personality based on subject and learning style"""
        personalities = {
            "math": {
                "visual": {
                    "tone": "analytical",
                    "pace": "moderate",
                    "examples": "geometric",
                    "encouragement": "logical",
                    "teaching_style": "step_by_step"
                },
                "auditory": {
                    "tone": "rhythmic",
                    "pace": "steady",
                    "examples": "verbal_patterns",
                    "encouragement": "musical",
                    "teaching_style": "repetitive"
                },
                "kinesthetic": {
                    "tone": "energetic",
                    "pace": "dynamic",
                    "examples": "hands_on",
                    "encouragement": "active",
                    "teaching_style": "interactive"
                }
            },
            "science": {
                "visual": {
                    "tone": "curious",
                    "pace": "measured",
                    "examples": "experimental",
                    "encouragement": "discovery",
                    "teaching_style": "demonstrative"
                },
                "auditory": {
                    "tone": "explanatory",
                    "pace": "conversational",
                    "examples": "narrative",
                    "encouragement": "questioning",
                    "teaching_style": "discussion"
                },
                "kinesthetic": {
                    "tone": "experimental",
                    "pace": "hands_on",
                    "examples": "practical",
                    "encouragement": "exploratory",
                    "teaching_style": "experiential"
                }
            },
            "language": {
                "visual": {
                    "tone": "literary",
                    "pace": "thoughtful",
                    "examples": "textual",
                    "encouragement": "creative",
                    "teaching_style": "analytical"
                },
                "auditory": {
                    "tone": "expressive",
                    "pace": "flowing",
                    "examples": "spoken",
                    "encouragement": "rhythmic",
                    "teaching_style": "oral"
                },
                "kinesthetic": {
                    "tone": "dramatic",
                    "pace": "dynamic",
                    "examples": "embodied",
                    "encouragement": "performative",
                    "teaching_style": "immersive"
                }
            },
            "history": {
                "visual": {
                    "tone": "narrative",
                    "pace": "storytelling",
                    "examples": "chronological",
                    "encouragement": "contextual",
                    "teaching_style": "timeline_based"
                },
                "auditory": {
                    "tone": "storytelling",
                    "pace": "engaging",
                    "examples": "anecdotal",
                    "encouragement": "dramatic",
                    "teaching_style": "narrative"
                },
                "kinesthetic": {
                    "tone": "immersive",
                    "pace": "experiential",
                    "examples": "role_playing",
                    "encouragement": "participatory",
                    "teaching_style": "simulation"
                }
            },
            "programming": {
                "visual": {
                    "tone": "systematic",
                    "pace": "methodical",
                    "examples": "code_examples",
                    "encouragement": "logical",
                    "teaching_style": "structured"
                },
                "auditory": {
                    "tone": "explanatory",
                    "pace": "clear",
                    "examples": "verbal_walkthroughs",
                    "encouragement": "problem_solving",
                    "teaching_style": "conversational"
                },
                "kinesthetic": {
                    "tone": "practical",
                    "pace": "interactive",
                    "examples": "coding_exercises",
                    "encouragement": "hands_on",
                    "teaching_style": "project_based"
                }
            }
        }
        
        # Default personality if subject/style not found
        default_personality = {
            "tone": "supportive",
            "pace": "moderate",
            "examples": "relatable",
            "encouragement": "positive",
            "teaching_style": "adaptive"
        }
        
        return personalities.get(subject, {}).get(learning_style, default_personality)
    
    def _select_voice_for_subject(self, subject: str) -> str:
        """Select appropriate voice based on subject"""
        voice_mapping = {
            "math": "analytical_female",
            "science": "curious_male",
            "language": "expressive_female",
            "history": "storyteller_male",
            "programming": "technical_female",
            "default": "friendly_neutral"
        }
        
        return voice_mapping.get(subject, voice_mapping["default"])
    
    def _get_scenario_context(self, scenario: str, language: str) -> Dict[str, Any]:
        """Get context information for language practice scenarios"""
        scenario_contexts = {
            "restaurant": {
                "setting": "A busy restaurant during dinner time",
                "role": "customer",
                "objectives": ["order food", "ask questions", "make requests"],
                "vocabulary_focus": ["food items", "dining etiquette", "payment"],
                "cultural_notes": f"Dining customs in {language}-speaking countries"
            },
            "business_meeting": {
                "setting": "Corporate conference room",
                "role": "meeting participant",
                "objectives": ["present ideas", "discuss plans", "make decisions"],
                "vocabulary_focus": ["business terms", "formal language", "presentations"],
                "cultural_notes": f"Business etiquette in {language}-speaking countries"
            },
            "travel": {
                "setting": "Airport, hotel, or tourist location",
                "role": "traveler",
                "objectives": ["get directions", "book accommodations", "ask for help"],
                "vocabulary_focus": ["travel terms", "directions", "accommodations"],
                "cultural_notes": f"Travel tips for {language}-speaking countries"
            },
            "shopping": {
                "setting": "Retail store or market",
                "role": "customer",
                "objectives": ["ask about products", "negotiate price", "make purchases"],
                "vocabulary_focus": ["shopping terms", "clothing", "prices"],
                "cultural_notes": f"Shopping customs in {language}-speaking countries"
            },
            "daily_conversation": {
                "setting": "Casual social environment",
                "role": "conversation partner",
                "objectives": ["small talk", "share experiences", "express opinions"],
                "vocabulary_focus": ["everyday terms", "emotions", "activities"],
                "cultural_notes": f"Social customs in {language}-speaking countries"
            }
        }
        
        return scenario_contexts.get(scenario, scenario_contexts["daily_conversation"])
    
    def _get_pronunciation_exercises(self, language: str, focus_area: str) -> List[Dict[str, Any]]:
        """Get pronunciation exercises for specific language and focus area"""
        exercises = {
            "en-US": {
                "vowels": [
                    {"text": "The cat sat on the mat", "focus": "short 'a' sound"},
                    {"text": "Pete eats sweet meat", "focus": "long 'e' sound"},
                    {"text": "I like to ride my bike", "focus": "long 'i' sound"}
                ],
                "consonants": [
                    {"text": "Red leather, yellow leather", "focus": "r/l distinction"},
                    {"text": "She sells seashells by the seashore", "focus": "s/sh sounds"},
                    {"text": "Think thick thoughts", "focus": "th sound"}
                ],
                "rhythm": [
                    {"text": "The beautiful butterfly flew by", "focus": "stress patterns"},
                    {"text": "Can you understand what I'm saying?", "focus": "sentence rhythm"},
                    {"text": "I want to go to the store", "focus": "linking sounds"}
                ]
            },
            "es-ES": {
                "vowels": [
                    {"text": "Ana ama a Papá", "focus": "'a' sound"},
                    {"text": "Este bebé bebe leche", "focus": "'e' sound"},
                    {"text": "Mi niño vive aquí", "focus": "'i' sound"}
                ],
                "consonants": [
                    {"text": "Rápido corren los carros por la carretera", "focus": "rolled 'r'"},
                    {"text": "José jugó en el jardín", "focus": "'j' sound"},
                    {"text": "Llueve en Sevilla", "focus": "'ll' sound"}
                ],
                "rhythm": [
                    {"text": "Mi mamá me mima mucho", "focus": "syllable timing"},
                    {"text": "¿Cómo está usted hoy?", "focus": "intonation patterns"},
                    {"text": "Vamos a la playa mañana", "focus": "linking"}
                ]
            }
        }
        
        default_exercises = [
            {"text": "Practice makes perfect", "focus": "general pronunciation"},
            {"text": "Speak clearly and slowly", "focus": "clarity"},
            {"text": "Listen and repeat", "focus": "repetition"}
        ]
        
        return exercises.get(language, {}).get(focus_area, default_exercises)
    
    async def get_user_active_sessions(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all active sessions for a user"""
        active_user_sessions = []
        
        for session_id, session_info in self.active_sessions.items():
            if session_info["user_id"] == user_id:
                # Get additional details from database
                db = SessionLocal()
                try:
                    db_session = db.query(LearningSession).filter(
                        LearningSession.omnidim_session_id == session_id
                    ).first()
                    
                    if db_session:
                        duration = (datetime.utcnow() - db_session.started_at).total_seconds()
                        active_user_sessions.append({
                            "session_id": session_id,
                            "type": db_session.type.value,
                            "subject": db_session.subject,
                            "language": db_session.language,
                            "duration_seconds": int(duration),
                            "started_at": db_session.started_at.isoformat()
                        })
                finally:
                    db.close()
        
        return active_user_sessions
    
    async def cleanup_expired_sessions(self, max_duration_hours: int = 24):
        """Clean up sessions that have been running too long"""
        current_time = datetime.utcnow()
        expired_sessions = []
        
        for session_id, session_info in self.active_sessions.items():
            session_duration = current_time - session_info["started_at"]
            if session_duration.total_seconds() > (max_duration_hours * 3600):
                expired_sessions.append(session_id)
        
        # Clean up expired sessions
        for session_id in expired_sessions:
            try:
                session_info = self.active_sessions[session_id]
                await self.end_session(session_id, session_info["user_id"])
                logger.info(f"Cleaned up expired session: {session_id}")
            except Exception as e:
                logger.error(f"Error cleaning up session {session_id}: {e}")
