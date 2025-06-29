from typing import Dict, List, Optional
import re
import logging

logger = logging.getLogger(__name__)

class VoiceHelpers:
    """Helper functions for voice interactions"""
    
    @staticmethod
    def extract_command(transcript: str) -> Optional[Dict]:
        """Extract voice commands from transcript"""
        transcript_lower = transcript.lower().strip()
        
        # Define command patterns
        commands = {
            "repeat": ["repeat", "say again", "what did you say"],
            "slower": ["slower", "slow down", "too fast"],
            "explain": ["explain", "what does that mean", "i don't understand"],
            "example": ["example", "give me an example", "for instance"],
            "test": ["test me", "quiz me", "check my understanding"],
            "help": ["help", "what can you do", "commands"],
            "stop": ["stop", "end session", "goodbye", "exit"]
        }
        
        for command, patterns in commands.items():
            for pattern in patterns:
                if pattern in transcript_lower:
                    return {
                        "command": command,
                        "original_text": transcript,
                        "confidence": 0.9  # Would be from speech recognition
                    }
        
        return None
    
    @staticmethod
    def format_voice_prompt(
        text: str,
        emotion: str = "neutral",
        pace: str = "normal"
    ) -> str:
        """Format text for voice synthesis with SSML hints"""
        # Add pauses for better comprehension
        text = re.sub(r'([.!?])', r'\1 <break time="500ms"/>', text)
        text = re.sub(r'([,;:])', r'\1 <break time="200ms"/>', text)
        
        # Adjust for emotion
        if emotion == "encouraging":
            text = f'<prosody pitch="+5%" rate="95%">{text}</prosody>'
        elif emotion == "calm":
            text = f'<prosody pitch="-5%" rate="90%">{text}</prosody>'
        
        # Wrap in speak tags
        return f'<speak>{text}</speak>'
    
    @staticmethod
    def generate_encouragement(
        performance_score: float,
        context: str = "general"
    ) -> str:
        """Generate encouraging message based on performance"""
        if performance_score >= 0.9:
            messages = [
                "Excellent work! You're really mastering this!",
                "Outstanding! Keep up the fantastic progress!",
                "You're doing amazingly well!"
            ]
        elif performance_score >= 0.7:
            messages = [
                "Good job! You're making great progress!",
                "Well done! You're getting better each time!",
                "Nice work! Keep practicing!"
            ]
        elif performance_score >= 0.5:
            messages = [
                "You're improving! Let's keep working on this.",
                "Good effort! Practice makes perfect.",
                "You're on the right track!"
            ]
        else:
            messages = [
                "Don't worry, learning takes time. Let's try again!",
                "Every expert was once a beginner. Keep going!",
                "This is challenging, but you can do it!"
            ]
        
        import random
        return random.choice(messages)
    
    @staticmethod
    def simplify_explanation(
        text: str,
        target_level: str = "intermediate"
    ) -> str:
        """Simplify explanation based on user level"""
        if target_level == "beginner":
            # Would use NLP to simplify
            # For now, just make shorter
            sentences = text.split('. ')
            if len(sentences) > 3:
                return '. '.join(sentences[:3]) + '.'
        
        return text