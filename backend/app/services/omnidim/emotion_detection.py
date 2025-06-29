from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np
from datetime import datetime, timedelta
import logging

from app.services.omnidim.client import OmnidimClient

logger = logging.getLogger(__name__)

class EmotionType(Enum):
    """Primary emotion categories"""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FEARFUL = "fearful"
    SURPRISED = "surprised"
    DISGUSTED = "disgusted"
    NEUTRAL = "neutral"
    EXCITED = "excited"
    CONFUSED = "confused"
    FRUSTRATED = "frustrated"
    CONFIDENT = "confident"
    ANXIOUS = "anxious"

class LearningState(Enum):
    """Learning-specific emotional states"""
    ENGAGED = "engaged"
    STRUGGLING = "struggling"
    BORED = "bored"
    OVERWHELMED = "overwhelmed"
    CONFIDENT = "confident"
    CURIOUS = "curious"
    FRUSTRATED = "frustrated"
    ACHIEVING = "achieving"

@dataclass
class EmotionResult:
    primary_emotion: EmotionType
    confidence: float
    all_emotions: Dict[str, float]
    arousal: float  # Energy level (0-1)
    valence: float  # Positive/negative (0-1)
    learning_state: Optional[LearningState] = None
    timestamp: datetime = None

@dataclass
class EmotionTrend:
    emotion_sequence: List[EmotionResult]
    dominant_emotion: EmotionType
    trend_direction: str  # "improving", "declining", "stable"
    engagement_score: float
    stress_indicators: List[str]

class EmotionDetector:
    """Advanced emotion detection and learning state analysis"""
    
    def __init__(self):
        self.client = OmnidimClient()
        self.emotion_history: Dict[str, List[EmotionResult]] = {}
        self.calibration_data: Dict[str, Dict] = {}
    
    async def detect_emotion(
        self,
        audio_data: bytes,
        session_id: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> EmotionResult:
        """Detect emotion from voice audio"""
        
        try:
            # Call Omnidim emotion analysis
            raw_result = await self.client.analyze_speech(
                audio_data=audio_data,
                analysis_type="emotion"
            )
            
            # Parse the result
            emotion_result = self._parse_emotion_result(raw_result)
            
            # Add learning state inference
            if session_id and user_id:
                emotion_result.learning_state = await self._infer_learning_state(
                    emotion_result, session_id, user_id
                )
            
            # Store in history
            if session_id:
                if session_id not in self.emotion_history:
                    self.emotion_history[session_id] = []
                self.emotion_history[session_id].append(emotion_result)
            
            return emotion_result
            
        except Exception as e:
            logger.error(f"Emotion detection failed: {e}")
            # Return neutral emotion as fallback
            return EmotionResult(
                primary_emotion=EmotionType.NEUTRAL,
                confidence=0.5,
                all_emotions={"neutral": 1.0},
                arousal=0.5,
                valence=0.5,
                timestamp=datetime.utcnow()
            )
    
    async def analyze_emotion_trend(
        self,
        session_id: str,
        time_window_minutes: int = 5
    ) -> EmotionTrend:
        """Analyze emotion trends over time"""
        
        if session_id not in self.emotion_history:
            return EmotionTrend(
                emotion_sequence=[],
                dominant_emotion=EmotionType.NEUTRAL,
                trend_direction="stable",
                engagement_score=0.5,
                stress_indicators=[]
            )
        
        # Get recent emotions within time window
        cutoff_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)
        recent_emotions = [
            emotion for emotion in self.emotion_history[session_id]
            if emotion.timestamp and emotion.timestamp >= cutoff_time
        ]
        
        if not recent_emotions:
            return EmotionTrend(
                emotion_sequence=[],
                dominant_emotion=EmotionType.NEUTRAL,
                trend_direction="stable",
                engagement_score=0.5,
                stress_indicators=[]
            )
        
        # Analyze trends
        dominant_emotion = self._find_dominant_emotion(recent_emotions)
        trend_direction = self._calculate_trend_direction(recent_emotions)
        engagement_score = self._calculate_engagement_score(recent_emotions)
        stress_indicators = self._detect_stress_indicators(recent_emotions)
        
        return EmotionTrend(
            emotion_sequence=recent_emotions,
            dominant_emotion=dominant_emotion,
            trend_direction=trend_direction,
            engagement_score=engagement_score,
            stress_indicators=stress_indicators
        )
    
    async def get_learning_recommendations(
        self,
        session_id: str,
        current_emotion: EmotionResult
    ) -> List[str]:
        """Get learning recommendations based on emotional state"""
        
        recommendations = []
        
        # Based on primary emotion
        if current_emotion.primary_emotion == EmotionType.FRUSTRATED:
            recommendations.extend([
                "Take a short break to reset",
                "Try breaking down the problem into smaller steps",
                "Consider switching to a different learning approach"
            ])
        
        elif current_emotion.primary_emotion == EmotionType.CONFUSED:
            recommendations.extend([
                "Ask for clarification or examples",
                "Review the previous concept before proceeding",
                "Try a different explanation or perspective"
            ])
        
        elif current_emotion.primary_emotion == EmotionType.BORED:
            recommendations.extend([
                "Increase the difficulty level",
                "Try a more interactive learning method",
                "Set a challenge or goal to work towards"
            ])
        
        elif current_emotion.primary_emotion == EmotionType.ANXIOUS:
            recommendations.extend([
                "Take deep breaths and relax",
                "Remember that mistakes are part of learning",
                "Focus on one step at a time"
            ])
        
        # Based on arousal and valence
        if current_emotion.arousal < 0.3:  # Low energy
            recommendations.append("Consider taking an energizing break")
        
        if current_emotion.valence < 0.3:  # Negative mood
            recommendations.append("Focus on positive reinforcement and encouragement")
        
        # Based on learning state
        if current_emotion.learning_state == LearningState.OVERWHELMED:
            recommendations.extend([
                "Reduce the complexity of current material",
                "Take a longer break",
                "Review fundamentals before continuing"
            ])
        
        elif current_emotion.learning_state == LearningState.STRUGGLING:
            recommendations.extend([
                "Provide additional examples",
                "Use alternative teaching methods",
                "Offer hints rather than direct answers"
            ])
        
        return recommendations
    
    def _parse_emotion_result(self, raw_result: Dict) -> EmotionResult:
        """Parse emotion detection result from Omnidim"""
        
        emotion_data = raw_result.get("emotion", {})
        
        # Map primary emotion string to enum
        primary_emotion_str = emotion_data.get("primary", "neutral")
        try:
            primary_emotion = EmotionType(primary_emotion_str.lower())
        except ValueError:
            primary_emotion = EmotionType.NEUTRAL
        
        return EmotionResult(
            primary_emotion=primary_emotion,
            confidence=emotion_data.get("confidence", 0.0),
            all_emotions=emotion_data.get("all_emotions", {}),
            arousal=emotion_data.get("arousal", 0.5),
            valence=emotion_data.get("valence", 0.5),
            timestamp=datetime.utcnow()
        )
    
    async def _infer_learning_state(
        self,
        emotion_result: EmotionResult,
        session_id: str,
        user_id: int
    ) -> LearningState:
        """Infer learning-specific state from emotion"""
        
        # Get recent emotion history for context
        recent_emotions = self.emotion_history.get(session_id, [])[-5:]  # Last 5 emotions
        
        # Rule-based inference
        if emotion_result.primary_emotion == EmotionType.FRUSTRATED:
            if emotion_result.arousal > 0.7:
                return LearningState.OVERWHELMED
            else:
                return LearningState.STRUGGLING
        
        elif emotion_result.primary_emotion == EmotionType.CONFUSED:
            return LearningState.STRUGGLING
        
        elif emotion_result.primary_emotion == EmotionType.EXCITED:
            return LearningState.ENGAGED
        
        elif emotion_result.primary_emotion == EmotionType.HAPPY:
            if emotion_result.arousal > 0.6:
                return LearningState.ACHIEVING
            else:
                return LearningState.ENGAGED
        
        elif emotion_result.primary_emotion == EmotionType.NEUTRAL:
            if emotion_result.arousal < 0.3:
                return LearningState.BORED
            else:
                return LearningState.ENGAGED
        
        elif emotion_result.primary_emotion == EmotionType.CONFIDENT:
            return LearningState.CONFIDENT
        
        elif emotion_result.primary_emotion == EmotionType.ANXIOUS:
            return LearningState.OVERWHELMED
        
        # Default to engaged if uncertain
        return LearningState.ENGAGED
    
    def _find_dominant_emotion(self, emotions: List[EmotionResult]) -> EmotionType:
        """Find the most frequent emotion in a sequence"""
        
        emotion_counts = {}
        for emotion in emotions:
            emotion_type = emotion.primary_emotion
            emotion_counts[emotion_type] = emotion_counts.get(emotion_type, 0) + 1
        
        if not emotion_counts:
            return EmotionType.NEUTRAL
        
        return max(emotion_counts, key=emotion_counts.get)
    
    def _calculate_trend_direction(self, emotions: List[EmotionResult]) -> str:
        """Calculate if emotions are trending positive, negative, or stable"""
        
        if len(emotions) < 3:
            return "stable"
        
        # Calculate valence trend
        valences = [emotion.valence for emotion in emotions]
        
        # Simple linear trend calculation
        x = list(range(len(valences)))
        trend_slope = np.polyfit(x, valences, 1)[0] if len(valences) > 1 else 0
        
        if trend_slope > 0.05:
            return "improving"
        elif trend_slope < -0.05:
            return "declining"
        else:
            return "stable"
    
    def _calculate_engagement_score(self, emotions: List[EmotionResult]) -> float:
        """Calculate overall engagement score from emotions"""
        
        if not emotions:
            return 0.5
        
        # Engagement factors
        arousal_avg = np.mean([emotion.arousal for emotion in emotions])
        positive_emotion_ratio = len([
            e for e in emotions 
            if e.primary_emotion in [EmotionType.HAPPY, EmotionType.EXCITED, EmotionType.CONFIDENT]
        ]) / len(emotions)
        
        # Penalize negative emotions
        negative_emotion_ratio = len([
            e for e in emotions 
            if e.primary_emotion in [EmotionType.FRUSTRATED, EmotionType.ANXIOUS, EmotionType.SAD]
        ]) / len(emotions)
        
        engagement_score = (
            arousal_avg * 0.4 +
            positive_emotion_ratio * 0.4 +
            (1 - negative_emotion_ratio) * 0.2
        )
        
        return max(0.0, min(1.0, engagement_score))
    
    def _detect_stress_indicators(self, emotions: List[EmotionResult]) -> List[str]:
        """Detect stress indicators from emotion sequence"""
        
        indicators = []
        
        if not emotions:
            return indicators
        
        # High arousal with negative valence
        high_stress_emotions = [
            e for e in emotions 
            if e.arousal > 0.7 and e.valence < 0.4
        ]
        if len(high_stress_emotions) / len(emotions) > 0.3:
            indicators.append("High stress levels detected")
        
        # Frequent frustration
        frustrated_emotions = [
            e for e in emotions 
            if e.primary_emotion == EmotionType.FRUSTRATED
        ]
        if len(frustrated_emotions) / len(emotions) > 0.4:
            indicators.append("Frequent frustration observed")
        
        # Declining engagement
        if len(emotions) >= 5:
            recent_engagement = self._calculate_engagement_score(emotions[-3:])
            earlier_engagement = self._calculate_engagement_score(emotions[:3])
            if recent_engagement < earlier_engagement - 0.2:
                indicators.append("Declining engagement trend")
        
        # Low confidence patterns
        low_confidence_emotions = [
            e for e in emotions 
            if e.confidence < 0.5
        ]
        if len(low_confidence_emotions) / len(emotions) > 0.6:
            indicators.append("Low confidence in emotional state detection")
        
        return indicators
    
    async def calibrate_user_baseline(
        self,
        user_id: int,
        baseline_audio_samples: List[bytes]
    ) -> Dict[str, Any]:
        """Calibrate emotion detection for specific user"""
        
        try:
            baseline_emotions = []
            
            for audio_sample in baseline_audio_samples:
                emotion_result = await self.detect_emotion(audio_sample)
                baseline_emotions.append(emotion_result)
            
            # Calculate user's baseline emotional characteristics
            baseline_data = {
                "average_arousal": np.mean([e.arousal for e in baseline_emotions]),
                "average_valence": np.mean([e.valence for e in baseline_emotions]),
                "dominant_baseline_emotion": self._find_dominant_emotion(baseline_emotions),
                "confidence_threshold": np.mean([e.confidence for e in baseline_emotions]),
                "calibration_date": datetime.utcnow().isoformat()
            }
            
            # Store calibration data
            self.calibration_data[str(user_id)] = baseline_data
            
            return baseline_data
            
        except Exception as e:
            logger.error(f"User calibration failed: {e}")
            raise
    
    def get_emotion_insights(
        self,
        session_id: str,
        time_window_minutes: int = 30
    ) -> Dict[str, Any]:
        """Get comprehensive emotion insights for a session"""
        
        if session_id not in self.emotion_history:
            return {
                "total_samples": 0,
                "emotion_distribution": {},
                "average_engagement": 0.5,
                "stress_level": "low",
                "recommendations": []
            }
        
        # Get emotions within time window
        cutoff_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)
        emotions = [
            e for e in self.emotion_history[session_id]
            if e.timestamp and e.timestamp >= cutoff_time
        ]
        
        if not emotions:
            return {
                "total_samples": 0,
                "emotion_distribution": {},
                "average_engagement": 0.5,
                "stress_level": "low",
                "recommendations": []
            }
        
        # Calculate emotion distribution
        emotion_counts = {}
        for emotion in emotions:
            emotion_type = emotion.primary_emotion.value
            emotion_counts[emotion_type] = emotion_counts.get(emotion_type, 0) + 1
        
        emotion_distribution = {
            emotion: count / len(emotions)
            for emotion, count in emotion_counts.items()
        }
        
        # Calculate metrics
        average_engagement = self._calculate_engagement_score(emotions)
        stress_indicators = self._detect_stress_indicators(emotions)
        
        # Determine stress level
        if len(stress_indicators) >= 3:
            stress_level = "high"
        elif len(stress_indicators) >= 1:
            stress_level = "medium"
        else:
            stress_level = "low"
        
        # Generate recommendations
        recommendations = []
        if average_engagement < 0.4:
            recommendations.append("Consider increasing interactivity to boost engagement")
        
        if stress_level == "high":
            recommendations.append("Take a break to reduce stress levels")
        
        if emotion_distribution.get("frustrated", 0) > 0.3:
            recommendations.append("Adjust difficulty level or teaching approach")
        
        return {
            "total_samples": len(emotions),
            "emotion_distribution": emotion_distribution,
            "average_engagement": average_engagement,
            "stress_level": stress_level,
            "stress_indicators": stress_indicators,
            "recommendations": recommendations,
            "session_duration_minutes": time_window_minutes
        }
