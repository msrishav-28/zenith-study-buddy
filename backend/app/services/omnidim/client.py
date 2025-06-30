import httpx
import asyncio
import json
import logging
from typing import Dict, Optional, Any, Callable
import websockets
from datetime import datetime

from app.config import settings

logger = logging.getLogger(__name__)

class OmnidimClient:
    """Client for interacting with Omnidim.io API"""
    
    def __init__(self):
        self.api_key = settings.OMNIDIM_API_KEY
        self.base_url = settings.OMNIDIM_API_URL
        self.ws_url = settings.OMNIDIM_WS_URL
        self._client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
        self._ws_connections: Dict[str, websockets.WebSocketClientProtocol] = {}
    
    async def create_voice_session(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new voice session with Omnidim"""
        try:
            response = await self._client.post(
                f"{self.base_url}/sessions/create",
                json=config
            )
            response.raise_for_status()
            result = response.json()
            return {
                "session_id": result.get("session_id"),
                "status": "created",
                "config": config
            }
        except Exception as e:
            logger.error(f"Failed to create voice session: {e}")
            raise
    
    async def end_voice_session(self, session_id: str) -> Dict[str, Any]:
        """End a voice session"""
        try:
            response = await self._client.post(
                f"{self.base_url}/sessions/{session_id}/end"
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to end voice session: {e}")
            raise
    
    async def pause_voice_session(self, session_id: str) -> Dict[str, Any]:
        """Pause a voice session"""
        try:
            response = await self._client.post(
                f"{self.base_url}/sessions/{session_id}/pause"
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to pause voice session: {e}")
            raise
    
    async def resume_voice_session(self, session_id: str) -> Dict[str, Any]:
        """Resume a voice session"""
        try:
            response = await self._client.post(
                f"{self.base_url}/sessions/{session_id}/resume"
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to resume voice session: {e}")
            raise
    
    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get session status"""
        try:
            response = await self._client.get(
                f"{self.base_url}/sessions/{session_id}/status"
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get session status: {e}")
            raise
    
    async def analyze_speech(
        self,
        audio_data: bytes,
        analysis_type: str = "full"
    ) -> Dict[str, Any]:
        """Analyze speech audio"""
        try:
            files = {"audio": ("audio.webm", audio_data, "audio/webm")}
            data = {"analysis_type": analysis_type}
            
            response = await self._client.post(
                f"{self.base_url}/analyze/speech",
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to analyze speech: {e}")
            raise
    
    async def connect_voice_stream(
        self,
        session_id: str,
        on_message_callback: Optional[Callable] = None
    ):
        """Connect to voice streaming WebSocket"""
        try:
            ws_uri = f"{self.ws_url}/voice/{session_id}?api_key={self.api_key}"
            
            async with websockets.connect(ws_uri) as websocket:
                self._ws_connections[session_id] = websocket
                
                async for message in websocket:
                    if on_message_callback:
                        if isinstance(message, bytes):
                            await on_message_callback({
                                "type": "audio",
                                "data": message
                            })
                        else:
                            data = json.loads(message)
                            await on_message_callback(data)
                            
        except Exception as e:
            logger.error(f"WebSocket connection error: {e}")
            raise
        finally:
            if session_id in self._ws_connections:
                del self._ws_connections[session_id]
    
    async def get_voice_models(self, language: Optional[str] = None) -> list:
        """Get available voice models"""
        params = {"language": language} if language else {}
        response = await self._client.get(
            f"{self.base_url}/voices",
            params=params
        )
        response.raise_for_status()
        return response.json()["voices"]
    
    async def close(self):
        """Close the HTTP client"""
        await self._client.aclose()