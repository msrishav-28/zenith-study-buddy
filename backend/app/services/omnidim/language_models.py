from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class LanguageModelManager:
    """Manages language-specific voice models in Omnidim"""
    
    @staticmethod
    def get_voice_for_language(language: str, gender: str = "female") -> str:
        """Get appropriate voice model for a language"""
        voice_map = {
            "en-US": {
                "female": "emily_us",
                "male": "james_us"
            },
            "en-GB": {
                "female": "sophie_uk",
                "male": "oliver_uk"
            },
            "es": {
                "female": "maria_es",
                "male": "carlos_es"
            },
            "fr": {
                "female": "claire_fr",
                "male": "pierre_fr"
            },
            "de": {
                "female": "anna_de",
                "male": "hans_de"
            },
            "it": {
                "female": "giulia_it",
                "male": "marco_it"
            },
            "pt": {
                "female": "ana_pt",
                "male": "joao_pt"
            },
            "zh": {
                "female": "mei_zh",
                "male": "wei_zh"
            },
            "ja": {
                "female": "yuki_ja",
                "male": "hiroshi_ja"
            },
            "ko": {
                "female": "jihye_ko",
                "male": "minho_ko"
            }
        }
        
        return voice_map.get(language, {}).get(gender, "emily_us")
    
    @staticmethod
    def get_language_features(language: str) -> List[str]:
        """Get available features for a language"""
        feature_map = {
            "en-US": [
                "pronunciation_scoring",
                "grammar_correction",
                "vocabulary_suggestions",
                "idiom_detection",
                "accent_coaching"
            ],
            "es": [
                "pronunciation_scoring",
                "grammar_correction",
                "vocabulary_suggestions",
                "conjugation_help",
                "regional_variations"
            ]
            # Add more languages
        }
        
        return feature_map.get(language, ["basic_transcription"])