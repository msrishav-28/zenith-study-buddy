from typing import Dict, List, Optional
import logging

from app.services.omnidim.client import OmnidimClient
from app.schemas.voice import PronunciationAnalysis

logger = logging.getLogger(__name__)

class SpeechAnalyzer:
    """Analyzes speech using Omnidim's speech analysis capabilities"""
    
    def __init__(self):
        self.client = OmnidimClient()
    
    async def analyze_pronunciation(
        self,
        audio_data: bytes,
        target_text: Optional[str],
        language: str,
        user_id: int
    ) -> PronunciationAnalysis:
        """Analyze pronunciation accuracy"""
        
        analysis_result = await self.client.analyze_speech(
            audio_data=audio_data,
            analysis_type="pronunciation"
        )
        
        # Process results into structured format
        pronunciation_analysis = PronunciationAnalysis(
            overall_score=analysis_result.get("overall_score", 0.0),
            phoneme_scores=analysis_result.get("phoneme_scores", []),
            fluency_score=analysis_result.get("fluency_score", 0.0),
            suggestions=self._generate_suggestions(analysis_result),
            audio_feedback_url=analysis_result.get("audio_feedback_url")
        )
        
        # Store analysis for progress tracking
        # TODO: Save to database
        
        return pronunciation_analysis
    
    async def get_pronunciation_guide(
        self,
        word: str,
        language: str
    ) -> Dict:
        """Get pronunciation guide for a word"""
        # This would call Omnidim's pronunciation guide API
        return {
            "word": word,
            "ipa": "[pronunciation]",
            "syllables": ["syl", "la", "bles"],
            "audio_url": f"https://api.omnidim.io/audio/pronounce/{word}",
            "tips": ["Focus on the first syllable", "The 'r' sound is soft"]
        }
    
    async def get_common_mistakes(
        self,
        target_language: str,
        native_language: str
    ) -> List[Dict]:
        """Get common pronunciation mistakes"""
        # Language pair specific mistakes
        mistakes_map = {
            ("en", "es"): [
                {
                    "sound": "th",
                    "description": "The 'th' sound doesn't exist in Spanish",
                    "examples": ["think", "that"],
                    "tip": "Place tongue between teeth"
                },
                {
                    "sound": "v/b",
                    "description": "Spanish speakers often confuse v and b",
                    "examples": ["very/berry", "vine/bine"],
                    "tip": "V uses teeth on lower lip"
                }
            ]
        }
        
        return mistakes_map.get((target_language, native_language), [])
    
    def _generate_suggestions(self, analysis_result: Dict) -> List[str]:
        """Generate improvement suggestions based on analysis"""
        suggestions = []
        
        if analysis_result.get("overall_score", 0) < 0.7:
            suggestions.append("Practice speaking more slowly and clearly")
        
        # Check specific phoneme issues
        phoneme_scores = analysis_result.get("phoneme_scores", [])
        for phoneme in phoneme_scores:
            if phoneme["score"] < 0.6:
                suggestions.append(f"Focus on pronouncing '{phoneme['phoneme']}' sounds")
        
        return suggestions