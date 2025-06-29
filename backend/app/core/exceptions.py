from fastapi import HTTPException, status

class OmnidimConnectionError(HTTPException):
    """Raised when Omnidim connection fails"""
    def __init__(self, detail: str = "Failed to connect to Omnidim service"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )

class SessionNotFoundError(HTTPException):
    """Raised when session is not found"""
    def __init__(self, session_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )

class InsufficientPermissionsError(HTTPException):
    """Raised when user lacks required permissions"""
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class InvalidAudioFormatError(HTTPException):
    """Raised when audio format is invalid"""
    def __init__(self, detail: str = "Invalid audio format"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )