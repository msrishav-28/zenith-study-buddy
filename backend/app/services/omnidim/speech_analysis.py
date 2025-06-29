from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json
import logging
from datetime import datetime

from app.services.omnidim.client import OmnidimClient

logger = logging.getLogger(__name__)

@dataclass
class PronunciationScore:
    phoneme: str
    accuracy: float
    confidence: float
    detected: str
    expected: str

@dataclass
class SpeechMetrics:
    wpm: float  # Words per minute
    pause_ratio: float  # Ratio of pauses to speech
    clarity_score: float  # Overall clarity (0-1)
    confidence_score: float  # Speaker confidence (0-1)
    emotion_primary: str  # Primary detected emotion
    emotion_confidence: float  # Confidence in emotion detection

@dataclass
class AnalysisResult:
    transcript: str
    pronunciation_scores: List[PronunciationScore]
    speech_metrics: SpeechMetrics
    suggestions: List[str]
    overall_score: float
    timestamp: datetime

class SpeechAnalyzer:
    """Analyzes speech data using Omnidim's AI capabilities"""
    
    def __init__(self):
        self.client = OmnidimClient()
        self.analysis_cache = {}
    
    async def analyze_pronunciation(
        self,
        audio_data: bytes,
        target_text: Optional[str] = None,
        language: str = "en-US"
    ) -> AnalysisResult:
        """Analyze pronunciation accuracy"""
        
        analysis_config = {
            "type": "pronunciation",
            "language": language,
            "target_text": target_text,
            "features": [
                "phoneme_accuracy",
                "word_stress",
                "intonation",
                "rhythm",
                "fluency"
            ]
        }
        
        try:
            # Send to Omnidim for analysis
            raw_result = await self.client.analyze_speech(
                audio_data=audio_data,
                analysis_type="pronunciation"
            )
            
            # Parse and structure the results
            return self._parse_pronunciation_result(raw_result)
            
        except Exception as e:
            logger.error(f"Pronunciation analysis failed: {e}")
            raise
    
    async def analyze_fluency(
        self,
        audio_data: bytes,
        language: str = "en-US"
    ) -> AnalysisResult:
        """Analyze speech fluency and natural flow"""
        
        try:
            raw_result = await self.client.analyze_speech(
                audio_data=audio_data,
                analysis_type="fluency"
            )
            
            return self._parse_fluency_result(raw_result)
            
        except Exception as e:
            logger.error(f"Fluency analysis failed: {e}")
            raise
    
    async def analyze_emotion(
        self,
        audio_data: bytes
    ) -> Dict[str, Any]:
        """Analyze emotional state from voice"""
        
        try:
            raw_result = await self.client.analyze_speech(
                audio_data=audio_data,
                analysis_type="emotion"
            )
            
            return {
                "primary_emotion": raw_result.get("emotion", {}).get("primary", "neutral"),
                "confidence": raw_result.get("emotion", {}).get("confidence", 0.0),
                "emotions": raw_result.get("emotion", {}).get("all_emotions", {}),
                "arousal": raw_result.get("emotion", {}).get("arousal", 0.5),
                "valence": raw_result.get("emotion", {}).get("valence", 0.5)
            }
            
        except Exception as e:
            logger.error(f"Emotion analysis failed: {e}")
            raise
    
    async def analyze_comprehensive(
        self,
        audio_data: bytes,
        target_text: Optional[str] = None,
        language: str = "en-US"
    ) -> AnalysisResult:
        """Perform comprehensive speech analysis"""
        
        try:
            raw_result = await self.client.analyze_speech(
                audio_data=audio_data,
                analysis_type="full"
            )
            
            return self._parse_comprehensive_result(raw_result, target_text)
            
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {e}")
            raise
    
    def _parse_pronunciation_result(self, raw_result: Dict) -> AnalysisResult:
        """Parse pronunciation analysis results"""
        
        # Extract pronunciation scores
        pronunciation_scores = []
        for phoneme_data in raw_result.get("pronunciation", {}).get("phonemes", []):
            pronunciation_scores.append(PronunciationScore(
                phoneme=phoneme_data.get("phoneme", ""),
                accuracy=phoneme_data.get("accuracy", 0.0),
                confidence=phoneme_data.get("confidence", 0.0),
                detected=phoneme_data.get("detected", ""),
                expected=phoneme_data.get("expected", "")
            ))
        
        # Extract speech metrics
        metrics_data = raw_result.get("metrics", {})
        speech_metrics = SpeechMetrics(
            wpm=metrics_data.get("wpm", 0.0),
            pause_ratio=metrics_data.get("pause_ratio", 0.0),
            clarity_score=metrics_data.get("clarity", 0.0),
            confidence_score=metrics_data.get("confidence", 0.0),
            emotion_primary=raw_result.get("emotion", {}).get("primary", "neutral"),
            emotion_confidence=raw_result.get("emotion", {}).get("confidence", 0.0)
        )
        
        # Generate suggestions
        suggestions = self._generate_pronunciation_suggestions(
            pronunciation_scores,
            speech_metrics
        )
        
        return AnalysisResult(
            transcript=raw_result.get("transcript", ""),
            pronunciation_scores=pronunciation_scores,
            speech_metrics=speech_metrics,
            suggestions=suggestions,
            overall_score=raw_result.get("overall_score", 0.0),
            timestamp=datetime.utcnow()
        )
    
    def _parse_fluency_result(self, raw_result: Dict) -> AnalysisResult:
        """Parse fluency analysis results"""
        
        metrics_data = raw_result.get("fluency", {})
        speech_metrics = SpeechMetrics(
            wpm=metrics_data.get("wpm", 0.0),
            pause_ratio=metrics_data.get("pause_ratio", 0.0),
            clarity_score=metrics_data.get("clarity", 0.0),
            confidence_score=metrics_data.get("confidence", 0.0),
            emotion_primary=raw_result.get("emotion", {}).get("primary", "neutral"),
            emotion_confidence=raw_result.get("emotion", {}).get("confidence", 0.0)
        )
        
        suggestions = self._generate_fluency_suggestions(speech_metrics)
        
        return AnalysisResult(
            transcript=raw_result.get("transcript", ""),
            pronunciation_scores=[],  # Not applicable for fluency-only analysis
            speech_metrics=speech_metrics,
            suggestions=suggestions,
            overall_score=metrics_data.get("fluency_score", 0.0),
            timestamp=datetime.utcnow()
        )
    
    def _parse_comprehensive_result(
        self,
        raw_result: Dict,
        target_text: Optional[str]
    ) -> AnalysisResult:
        """Parse comprehensive analysis results"""
        
        # Combine pronunciation and fluency parsing
        pronunciation_scores = []
        if "pronunciation" in raw_result:
            for phoneme_data in raw_result["pronunciation"].get("phonemes", []):
                pronunciation_scores.append(PronunciationScore(
                    phoneme=phoneme_data.get("phoneme", ""),
                    accuracy=phoneme_data.get("accuracy", 0.0),
                    confidence=phoneme_data.get("confidence", 0.0),
                    detected=phoneme_data.get("detected", ""),
                    expected=phoneme_data.get("expected", "")
                ))
        
        metrics_data = raw_result.get("metrics", {})
        speech_metrics = SpeechMetrics(
            wpm=metrics_data.get("wpm", 0.0),
            pause_ratio=metrics_data.get("pause_ratio", 0.0),
            clarity_score=metrics_data.get("clarity", 0.0),
            confidence_score=metrics_data.get("confidence", 0.0),
            emotion_primary=raw_result.get("emotion", {}).get("primary", "neutral"),
            emotion_confidence=raw_result.get("emotion", {}).get("confidence", 0.0)
        )
        
        # Generate comprehensive suggestions
        suggestions = []
        suggestions.extend(self._generate_pronunciation_suggestions(
            pronunciation_scores, speech_metrics
        ))
        suggestions.extend(self._generate_fluency_suggestions(speech_metrics))
        
        return AnalysisResult(
            transcript=raw_result.get("transcript", ""),
            pronunciation_scores=pronunciation_scores,
            speech_metrics=speech_metrics,
            suggestions=list(set(suggestions)),  # Remove duplicates
            overall_score=raw_result.get("overall_score", 0.0),
            timestamp=datetime.utcnow()
        )
    
    def _generate_pronunciation_suggestions(
        self,
        pronunciation_scores: List[PronunciationScore],
        speech_metrics: SpeechMetrics
    ) -> List[str]:
        """Generate pronunciation improvement suggestions"""
        
        suggestions = []
        
        # Check for low-scoring phonemes
        low_accuracy_phonemes = [
            score for score in pronunciation_scores
            if score.accuracy < 0.7
        ]
        
        if low_accuracy_phonemes:
            problem_phonemes = ", ".join([p.phoneme for p in low_accuracy_phonemes[:3]])
            suggestions.append(
                f"Focus on improving pronunciation of: {problem_phonemes}"
            )
        
        # Check speech rate
        if speech_metrics.wpm > 180:
            suggestions.append("Try speaking more slowly for better clarity")
        elif speech_metrics.wpm < 120:
            suggestions.append("Try speaking a bit faster for more natural rhythm")
        
        # Check clarity
        if speech_metrics.clarity_score < 0.7:
            suggestions.append("Focus on articulating words more clearly")
        
        return suggestions
    
    def _generate_fluency_suggestions(
        self,
        speech_metrics: SpeechMetrics
    ) -> List[str]:
        """Generate fluency improvement suggestions"""
        
        suggestions = []
        
        # Check pause patterns
        if speech_metrics.pause_ratio > 0.3:
            suggestions.append("Try to reduce long pauses between words")
        
        # Check confidence
        if speech_metrics.confidence_score < 0.6:
            suggestions.append("Practice speaking with more confidence and conviction")
        
        # Check overall fluency
        if speech_metrics.wpm < 100:
            suggestions.append("Practice speaking more fluently without hesitation")
        
        return suggestions
    
    async def get_analysis_history(
        self,
        user_id: int,
        session_id: Optional[str] = None,
        limit: int = 10
    ) -> List[AnalysisResult]:
        """Get previous analysis results for a user"""
        
        # This would typically query a database
        # For now, return empty list as placeholder
        return []
    
    async def compare_progress(
        self,
        user_id: int,
        current_result: AnalysisResult,
        days_back: int = 7
    ) -> Dict[str, Any]:
        """Compare current analysis with historical progress"""
        
        # Placeholder for progress comparison logic
        return {
            "improvement_trend": "improving",
            "score_change": 0.05,
            "areas_improved": ["pronunciation", "fluency"],
            "areas_to_focus": ["clarity"]
        }
