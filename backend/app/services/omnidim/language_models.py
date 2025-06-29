from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import logging
from datetime import datetime

from app.services.omnidim.client import OmnidimClient

logger = logging.getLogger(__name__)

class LanguageLevel(Enum):
    """Language proficiency levels"""
    BEGINNER = "beginner"
    ELEMENTARY = "elementary"
    INTERMEDIATE = "intermediate"
    UPPER_INTERMEDIATE = "upper_intermediate"
    ADVANCED = "advanced"
    NATIVE = "native"

class PracticeScenario(Enum):
    """Language practice scenarios"""
    DAILY_CONVERSATION = "daily_conversation"
    BUSINESS_MEETING = "business_meeting"
    TRAVEL = "travel"
    RESTAURANT = "restaurant"
    SHOPPING = "shopping"
    JOB_INTERVIEW = "job_interview"
    ACADEMIC = "academic"
    HEALTHCARE = "healthcare"
    SOCIAL_EVENT = "social_event"
    PHONE_CALL = "phone_call"

@dataclass
class LanguageModel:
    """Language model configuration"""
    language_code: str
    language_name: str
    voice_id: str
    accent: str
    gender: str
    age_range: str
    personality: Dict[str, Any]
    supported_scenarios: List[PracticeScenario]
    proficiency_levels: List[LanguageLevel]

@dataclass
class ConversationContext:
    """Context for language conversation"""
    scenario: PracticeScenario
    target_language: str
    native_language: str
    proficiency_level: LanguageLevel
    learning_objectives: List[str]
    cultural_context: Dict[str, Any]
    vocabulary_focus: List[str]
    grammar_focus: List[str]

@dataclass
class LanguageFeedback:
    """Feedback for language practice"""
    grammar_score: float
    vocabulary_score: float
    pronunciation_score: float
    fluency_score: float
    cultural_appropriateness: float
    corrections: List[Dict[str, str]]
    suggestions: List[str]
    vocabulary_used: List[str]
    new_vocabulary: List[Dict[str, str]]

class LanguageModelManager:
    """Manages language models and conversation contexts"""
    
    def __init__(self):
        self.client = OmnidimClient()
        self.available_models: Dict[str, LanguageModel] = {}
        self.conversation_contexts: Dict[str, ConversationContext] = {}
        self._initialize_language_models()
    
    def _initialize_language_models(self):
        """Initialize available language models"""
        
        # English models
        self.available_models["en-US"] = LanguageModel(
            language_code="en-US",
            language_name="English (US)",
            voice_id="native_en_us_female",
            accent="American",
            gender="female",
            age_range="25-35",
            personality={
                "tone": "friendly",
                "pace": "moderate",
                "formality": "casual",
                "patience": "high"
            },
            supported_scenarios=list(PracticeScenario),
            proficiency_levels=list(LanguageLevel)
        )
        
        # Spanish models
        self.available_models["es-ES"] = LanguageModel(
            language_code="es-ES",
            language_name="Spanish (Spain)",
            voice_id="native_es_es_male",
            accent="Iberian",
            gender="male",
            age_range="30-40",
            personality={
                "tone": "warm",
                "pace": "moderate",
                "formality": "polite",
                "patience": "very_high"
            },
            supported_scenarios=list(PracticeScenario),
            proficiency_levels=list(LanguageLevel)
        )
        
        # French models
        self.available_models["fr-FR"] = LanguageModel(
            language_code="fr-FR",
            language_name="French (France)",
            voice_id="native_fr_fr_female",
            accent="Parisian",
            gender="female",
            age_range="28-38",
            personality={
                "tone": "elegant",
                "pace": "moderate",
                "formality": "formal",
                "patience": "high"
            },
            supported_scenarios=list(PracticeScenario),
            proficiency_levels=list(LanguageLevel)
        )
        
        # German models
        self.available_models["de-DE"] = LanguageModel(
            language_code="de-DE",
            language_name="German (Germany)",
            voice_id="native_de_de_male",
            accent="Standard German",
            gender="male",
            age_range="32-42",
            personality={
                "tone": "professional",
                "pace": "careful",
                "formality": "formal",
                "patience": "very_high"
            },
            supported_scenarios=list(PracticeScenario),
            proficiency_levels=list(LanguageLevel)
        )
        
        # Add more languages as needed
        self._add_additional_languages()
    
    def _add_additional_languages(self):
        """Add additional language models"""
        
        # Italian
        self.available_models["it-IT"] = LanguageModel(
            language_code="it-IT",
            language_name="Italian (Italy)",
            voice_id="native_it_it_female",
            accent="Standard Italian",
            gender="female",
            age_range="26-36",
            personality={
                "tone": "expressive",
                "pace": "moderate",
                "formality": "casual",
                "patience": "high"
            },
            supported_scenarios=list(PracticeScenario),
            proficiency_levels=list(LanguageLevel)
        )
        
        # Portuguese
        self.available_models["pt-BR"] = LanguageModel(
            language_code="pt-BR",
            language_name="Portuguese (Brazil)",
            voice_id="native_pt_br_male",
            accent="Brazilian",
            gender="male",
            age_range="29-39",
            personality={
                "tone": "friendly",
                "pace": "relaxed",
                "formality": "casual",
                "patience": "very_high"
            },
            supported_scenarios=list(PracticeScenario),
            proficiency_levels=list(LanguageLevel)
        )
        
        # Japanese
        self.available_models["ja-JP"] = LanguageModel(
            language_code="ja-JP",
            language_name="Japanese (Japan)",
            voice_id="native_ja_jp_female",
            accent="Tokyo",
            gender="female",
            age_range="25-35",
            personality={
                "tone": "polite",
                "pace": "careful",
                "formality": "formal",
                "patience": "extremely_high"
            },
            supported_scenarios=list(PracticeScenario),
            proficiency_levels=list(LanguageLevel)
        )
        
        # Mandarin Chinese
        self.available_models["zh-CN"] = LanguageModel(
            language_code="zh-CN",
            language_name="Mandarin Chinese (China)",
            voice_id="native_zh_cn_female",
            accent="Beijing",
            gender="female",
            age_range="27-37",
            personality={
                "tone": "patient",
                "pace": "slow",
                "formality": "polite",
                "patience": "extremely_high"
            },
            supported_scenarios=list(PracticeScenario),
            proficiency_levels=list(LanguageLevel)
        )
    
    async def get_available_languages(self) -> List[Dict[str, Any]]:
        """Get list of available languages for practice"""
        
        return [
            {
                "code": model.language_code,
                "name": model.language_name,
                "accent": model.accent,
                "voice_gender": model.gender,
                "supported_scenarios": [scenario.value for scenario in model.supported_scenarios],
                "proficiency_levels": [level.value for level in model.proficiency_levels]
            }
            for model in self.available_models.values()
        ]
    
    async def create_conversation_context(
        self,
        session_id: str,
        target_language: str,
        native_language: str,
        scenario: str,
        proficiency_level: str,
        learning_objectives: List[str] = None
    ) -> ConversationContext:
        """Create conversation context for language practice"""
        
        try:
            scenario_enum = PracticeScenario(scenario)
            proficiency_enum = LanguageLevel(proficiency_level)
        except ValueError as e:
            raise ValueError(f"Invalid scenario or proficiency level: {e}")
        
        # Get cultural context for the scenario
        cultural_context = self._get_cultural_context(target_language, scenario_enum)
        
        # Get vocabulary and grammar focus
        vocabulary_focus = self._get_vocabulary_focus(scenario_enum, proficiency_enum)
        grammar_focus = self._get_grammar_focus(target_language, proficiency_enum)
        
        context = ConversationContext(
            scenario=scenario_enum,
            target_language=target_language,
            native_language=native_language,
            proficiency_level=proficiency_enum,
            learning_objectives=learning_objectives or [],
            cultural_context=cultural_context,
            vocabulary_focus=vocabulary_focus,
            grammar_focus=grammar_focus
        )
        
        # Store context
        self.conversation_contexts[session_id] = context
        
        return context
    
    async def get_scenario_prompt(
        self,
        session_id: str,
        context: ConversationContext
    ) -> str:
        """Generate initial prompt for conversation scenario"""
        
        scenario_prompts = {
            PracticeScenario.DAILY_CONVERSATION: self._get_daily_conversation_prompt,
            PracticeScenario.BUSINESS_MEETING: self._get_business_meeting_prompt,
            PracticeScenario.TRAVEL: self._get_travel_prompt,
            PracticeScenario.RESTAURANT: self._get_restaurant_prompt,
            PracticeScenario.SHOPPING: self._get_shopping_prompt,
            PracticeScenario.JOB_INTERVIEW: self._get_job_interview_prompt,
            PracticeScenario.ACADEMIC: self._get_academic_prompt,
            PracticeScenario.HEALTHCARE: self._get_healthcare_prompt,
            PracticeScenario.SOCIAL_EVENT: self._get_social_event_prompt,
            PracticeScenario.PHONE_CALL: self._get_phone_call_prompt
        }
        
        prompt_generator = scenario_prompts.get(context.scenario)
        if prompt_generator:
            return prompt_generator(context)
        else:
            return self._get_default_prompt(context)
    
    async def analyze_language_response(
        self,
        audio_data: bytes,
        session_id: str,
        expected_language: str
    ) -> LanguageFeedback:
        """Analyze language practice response"""
        
        try:
            # Get conversation context
            context = self.conversation_contexts.get(session_id)
            if not context:
                raise ValueError(f"No conversation context found for session {session_id}")
            
            # Call Omnidim for comprehensive language analysis
            analysis_result = await self.client.analyze_speech(
                audio_data=audio_data,
                analysis_type="language_practice"
            )
            
            # Parse and structure the feedback
            return self._parse_language_feedback(analysis_result, context)
            
        except Exception as e:
            logger.error(f"Language analysis failed: {e}")
            raise
    
    def _get_cultural_context(
        self,
        language: str,
        scenario: PracticeScenario
    ) -> Dict[str, Any]:
        """Get cultural context for language and scenario"""
        
        cultural_contexts = {
            "es-ES": {
                PracticeScenario.RESTAURANT: {
                    "greeting": "Formal greeting expected",
                    "payment": "Cash is common, tipping is appreciated",
                    "time": "Lunch is typically late (2-3 PM)"
                },
                PracticeScenario.BUSINESS_MEETING: {
                    "formality": "High formality expected",
                    "hierarchy": "Respect for authority important",
                    "time": "Punctuality valued"
                }
            },
            "fr-FR": {
                PracticeScenario.RESTAURANT: {
                    "greeting": "Always greet when entering",
                    "bread": "Bread is free and expected",
                    "wine": "Wine selection is important"
                },
                PracticeScenario.SOCIAL_EVENT: {
                    "greeting": "Cheek kissing common",
                    "conversation": "Avoid personal topics initially",
                    "wine": "Wine appreciation valued"
                }
            },
            # Add more cultural contexts
        }
        
        return cultural_contexts.get(language, {}).get(scenario, {})
    
    def _get_vocabulary_focus(
        self,
        scenario: PracticeScenario,
        proficiency: LanguageLevel
    ) -> List[str]:
        """Get vocabulary focus for scenario and proficiency"""
        
        vocabulary_sets = {
            PracticeScenario.RESTAURANT: {
                LanguageLevel.BEGINNER: [
                    "menu", "order", "food", "drink", "please", "thank you",
                    "bill", "water", "bread", "table"
                ],
                LanguageLevel.INTERMEDIATE: [
                    "appetizer", "main course", "dessert", "recommendation",
                    "allergic", "vegetarian", "spicy", "medium", "well-done"
                ],
                LanguageLevel.ADVANCED: [
                    "sommelier", "pairing", "preparation", "ingredients",
                    "culinary", "authentic", "signature dish", "ambiance"
                ]
            },
            PracticeScenario.BUSINESS_MEETING: {
                LanguageLevel.BEGINNER: [
                    "meeting", "agenda", "project", "deadline", "team",
                    "budget", "report", "presentation", "schedule"
                ],
                LanguageLevel.INTERMEDIATE: [
                    "quarterly", "revenue", "objectives", "strategy",
                    "implementation", "stakeholders", "resources", "timeline"
                ],
                LanguageLevel.ADVANCED: [
                    "deliverables", "synergies", "optimization", "scalability",
                    "ROI", "KPIs", "benchmarking", "paradigm shift"
                ]
            }
            # Add more scenarios
        }
        
        return vocabulary_sets.get(scenario, {}).get(proficiency, [])
    
    def _get_grammar_focus(
        self,
        language: str,
        proficiency: LanguageLevel
    ) -> List[str]:
        """Get grammar focus for language and proficiency"""
        
        grammar_focus = {
            "es-ES": {
                LanguageLevel.BEGINNER: [
                    "present tense", "ser vs estar", "gender agreement",
                    "basic questions", "numbers"
                ],
                LanguageLevel.INTERMEDIATE: [
                    "past tenses", "subjunctive mood", "conditional",
                    "object pronouns", "relative clauses"
                ],
                LanguageLevel.ADVANCED: [
                    "advanced subjunctive", "passive voice", "complex conditionals",
                    "idiomatic expressions", "register variation"
                ]
            },
            "fr-FR": {
                LanguageLevel.BEGINNER: [
                    "present tense", "avoir vs être", "gender agreement",
                    "basic questions", "partitive articles"
                ],
                LanguageLevel.INTERMEDIATE: [
                    "past tenses", "subjunctive", "conditional",
                    "pronouns", "relative clauses"
                ],
                LanguageLevel.ADVANCED: [
                    "advanced subjunctive", "literary tenses", "complex syntax",
                    "stylistic variations", "formal register"
                ]
            }
            # Add more languages
        }
        
        return grammar_focus.get(language, {}).get(proficiency, [])
    
    def _get_daily_conversation_prompt(self, context: ConversationContext) -> str:
        """Generate daily conversation prompt"""
        return f"Let's have a casual conversation in {context.target_language}. I'll start by asking about your day. Feel free to ask me questions too!"
    
    def _get_business_meeting_prompt(self, context: ConversationContext) -> str:
        """Generate business meeting prompt"""
        return f"Welcome to our business meeting. Let's discuss the quarterly project updates in {context.target_language}. Shall we begin with the agenda?"
    
    def _get_travel_prompt(self, context: ConversationContext) -> str:
        """Generate travel scenario prompt"""
        return f"You've just arrived at the airport in a {context.target_language}-speaking country. I'm at the information desk. How can I help you?"
    
    def _get_restaurant_prompt(self, context: ConversationContext) -> str:
        """Generate restaurant scenario prompt"""
        return f"Welcome to our restaurant! I'm your server today. Would you like to see the menu, or do you have any questions about our dishes?"
    
    def _get_shopping_prompt(self, context: ConversationContext) -> str:
        """Generate shopping scenario prompt"""
        return f"Welcome to our store! I'm here to help you find what you're looking for. What can I assist you with today?"
    
    def _get_job_interview_prompt(self, context: ConversationContext) -> str:
        """Generate job interview prompt"""
        return f"Thank you for coming in today. Let's begin the interview. Could you start by telling me about yourself and your background?"
    
    def _get_academic_prompt(self, context: ConversationContext) -> str:
        """Generate academic scenario prompt"""
        return f"Let's discuss academic topics in {context.target_language}. What subject would you like to explore today?"
    
    def _get_healthcare_prompt(self, context: ConversationContext) -> str:
        """Generate healthcare scenario prompt"""
        return f"I'm the doctor/nurse. Please describe your symptoms or concerns, and I'll do my best to help."
    
    def _get_social_event_prompt(self, context: ConversationContext) -> str:
        """Generate social event prompt"""
        return f"Welcome to the party! It's nice to meet you. How do you know the host?"
    
    def _get_phone_call_prompt(self, context: ConversationContext) -> str:
        """Generate phone call prompt"""
        return f"Ring ring... Hello, this is a practice phone call in {context.target_language}. How are you today?"
    
    def _get_default_prompt(self, context: ConversationContext) -> str:
        """Generate default prompt"""
        return f"Let's practice {context.target_language} together! I'm here to help you improve your conversation skills."
    
    def _parse_language_feedback(
        self,
        analysis_result: Dict,
        context: ConversationContext
    ) -> LanguageFeedback:
        """Parse language analysis results into structured feedback"""
        
        # Extract scores
        scores = analysis_result.get("scores", {})
        
        # Extract corrections
        corrections = []
        for correction in analysis_result.get("corrections", []):
            corrections.append({
                "original": correction.get("original", ""),
                "corrected": correction.get("corrected", ""),
                "explanation": correction.get("explanation", ""),
                "type": correction.get("type", "grammar")
            })
        
        # Extract vocabulary
        vocabulary_data = analysis_result.get("vocabulary", {})
        vocabulary_used = vocabulary_data.get("detected", [])
        new_vocabulary = [
            {
                "word": item.get("word", ""),
                "definition": item.get("definition", ""),
                "example": item.get("example", "")
            }
            for item in vocabulary_data.get("suggestions", [])
        ]
        
        # Generate suggestions
        suggestions = self._generate_language_suggestions(analysis_result, context)
        
        return LanguageFeedback(
            grammar_score=scores.get("grammar", 0.0),
            vocabulary_score=scores.get("vocabulary", 0.0),
            pronunciation_score=scores.get("pronunciation", 0.0),
            fluency_score=scores.get("fluency", 0.0),
            cultural_appropriateness=scores.get("cultural", 1.0),
            corrections=corrections,
            suggestions=suggestions,
            vocabulary_used=vocabulary_used,
            new_vocabulary=new_vocabulary
        )
    
    def _generate_language_suggestions(
        self,
        analysis_result: Dict,
        context: ConversationContext
    ) -> List[str]:
        """Generate learning suggestions based on analysis"""
        
        suggestions = []
        scores = analysis_result.get("scores", {})
        
        # Grammar suggestions
        if scores.get("grammar", 1.0) < 0.7:
            suggestions.append(f"Focus on {context.target_language} grammar rules, especially {', '.join(context.grammar_focus[:2])}")
        
        # Vocabulary suggestions
        if scores.get("vocabulary", 1.0) < 0.7:
            suggestions.append(f"Expand your vocabulary related to {context.scenario.value}")
        
        # Pronunciation suggestions
        if scores.get("pronunciation", 1.0) < 0.7:
            suggestions.append("Practice pronunciation with native speakers or audio resources")
        
        # Fluency suggestions
        if scores.get("fluency", 1.0) < 0.7:
            suggestions.append("Practice speaking more regularly to improve fluency")
        
        return suggestions
