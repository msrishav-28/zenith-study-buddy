from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import logging

from app.core.dependencies import get_current_user_ws
from app.services.omnidim.client import OmnidimClient
from app.api.websocket.voice_stream_handler import VoiceStreamHandler

router = APIRouter()
logger = logging.getLogger(__name__)

# Global handler instance
voice_handler = VoiceStreamHandler()

@router.websocket("/voice/{session_id}")
async def voice_stream_endpoint(
    websocket: WebSocket,
    session_id: str,
    token: str = None
):
    """WebSocket endpoint for voice streaming"""
    try:
        # Authenticate user from token
        user = await get_current_user_ws(token)
        if not user:
            await websocket.close(code=1008, reason="Unauthorized")
            return
        
        # Handle voice stream
        await voice_handler.handle_connection(
            websocket=websocket,
            session_id=session_id,
            user_id=user.id
        )
        
    except WebSocketDisconnect:
        logger.info(f"Client disconnected from session {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=1011, reason="Internal error")