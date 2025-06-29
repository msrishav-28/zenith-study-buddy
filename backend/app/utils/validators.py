from typing import Optional
import re
from email_validator import validate_email, EmailNotValidError

class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username format"""
        # 3-20 characters, alphanumeric and underscore only
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, Optional[str]]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        
        return True, None
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    @staticmethod
    def validate_session_type(session_type: str) -> bool:
        """Validate session type"""
        valid_types = ["tutor", "language_practice", "exam_prep", "pronunciation"]
        return session_type in valid_types
    
    @staticmethod
    def validate_language_code(code: str) -> bool:
        """Validate language code"""
        valid_codes = [
            "en-US", "en-GB", "es", "fr", "de", "it", "pt", 
            "zh", "ja", "ko", "ar", "hi", "ru"
        ]
        return code in valid_codes
    
    @staticmethod
    def validate_difficulty(difficulty: str) -> bool:
        """Validate difficulty level"""
        valid_levels = ["beginner", "elementary", "intermediate", "advanced", "expert"]
        return difficulty in valid_levels
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Sanitize text input"""
        # Remove any potential script tags or HTML
        text = re.sub(r'<[^>]*>', '', text)
        # Remove excessive whitespace
        text = ' '.join(text.split())
        return text.strip()