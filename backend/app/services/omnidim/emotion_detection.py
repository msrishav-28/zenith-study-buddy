from typing import Dict, Optional
import logging

from app.services.omnidim.client import OmnidimClient

logger = logging.getLogger(__name__)

class EmotionDetector:
    """Detects emotions from voice using Omnidim"""
    
    def __init__(self):
        self.client = OmnidimClient()
    
    async def detect_emotion(self, audio_data: bytes) -> Dict:
        """Detect emotion from audio"""
        result = await self.client.analyze_speech(
            audio_data=audio_data,
            analysis_type="emotion"
        )
        
        return {
            "primary_emotion": result.get("primary_emotion", "neutral"),
            "confidence": result.get("confidence", 0.0),
            "all_emotions": result.get("emotion_scores", {})
        }
    
    def get_teaching_adaptation(self, emotion: str) -> Dict:
        """Get teaching adaptations based on detected emotion"""
        adaptations = {
            "confused": {
                "pace": "slower",
                "explanation_style": "step_by_step",
                "encouragement_level": "high",
                "suggestion": "Let me break this down into smaller parts..."
            },
            "frustrated": {
                "pace": "slower",
                "explanation_style": "alternative_approach",
                "encouragement_level": "very_high",
                "suggestion": "I understand this is challenging. Let's try a different approach..."
            },
            "bored": {
                "pace": "faster",
                "explanation_style": "engaging_examples",
                "encouragement_level": "moderate",
                "suggestion": "Let's make this more interesting with a real-world example..."
            },
            "excited": {
                "pace": "matching",
                "explanation_style": "challenging",
                "encouragement_level": "moderate",
                "suggestion": "Great energy! Ready for something more advanced?"
            }
        }
        
        return adaptations.get(emotion, {
            "pace": "normal",
            "explanation_style": "standard",
            "encouragement_level": "moderate",
            "suggestion": "Let's continue..."
        })