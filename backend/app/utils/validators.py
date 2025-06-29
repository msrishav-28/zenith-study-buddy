from typing import Optional
import re

class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username format"""
        # 3-20 characters, alphanumeric and underscore only
        pattern = r'^[a-zA-Z0-9_]{3,20}                "auditory": {
                    "tone": "rhythmic",
                    "pace": "varied",
                    "examples": "pattern-based",
                    "encouragement": "verbal"
                }
            },
            "language": {
                "visual": {
                    "tone": "descriptive",
                    "pace": "steady",
                    "examples": "imagery-rich",
                    "encouragement": "expressive"
                }
            }
        }
        
        return personalities.get(subject, {}).get(learning_style, {
            "tone": "friendly",
            "pace": "adaptive",
            "examples": "practical",
            "encouragement": "supportive"
        })
    
    def _select_voice_for_subject(self, subject: str) -> str:
        """Select appropriate voice model for subject"""
        voice_mapping = {
            "math": "tutor_analytical_sarah",
            "science": "tutor_curious_james",
            "language": "tutor_expressive_emma",
            "history": "tutor_narrative_michael",
            "programming": "tutor_technical_alex"
        }
        return voice_mapping.get(subject, "tutor_friendly_sarah")
    
    def _get_scenario_context(self, scenario: str, language: str) -> Dict:
        """Get context for language practice scenario"""
        contexts = {
            "restaurant": {
                "setting": "casual_dining",
                "vocabulary_focus": ["food", "ordering", "preferences"],
                "cultural_notes": ["tipping", "etiquette"]
            },
            "business": {
                "setting": "professional",
                "vocabulary_focus": ["formal", "negotiations", "presentations"],
                "cultural_notes": ["greetings", "hierarchy"]
            }
        }
        return contexts.get(scenario, {})