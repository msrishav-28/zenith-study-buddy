import httpx
import asyncio
import websockets
import json
from typing import Dict, Optional, AsyncGenerator, Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class OmnidimClient:
    """Main client for Omnidim.io Voice AI Platform"""
    
    def __init__(self):
        self.api_key = settings.OMNIDIM_API_KEY
        self.base_url = settings.OMNIDIM_API_URL
        self.ws_url = settings.OMNIDIM_WS_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self._client = httpx.AsyncClient(headers=self.headers, timeout=30.0)
    
    async def create_voice_session(
        self,
        session_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new voice session with Omnidim"""
        try:
            response = await self._client.post(
                f"{self.base_url}/sessions/create",
                json=session_config
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to create voice session: {e}")
            raise
    
    async def connect_voice_stream(
        self,
        session_id: str,
        on_message_callback: callable
    ):
        """Connect to Omnidim WebSocket for real-time voice streaming"""
        ws_uri = f"{self.ws_url}/stream/{session_id}?api_key={self.api_key}"
        
        async with websockets.connect(ws_uri) as websocket:
            logger.info(f"Connected to Omnidim voice stream: {session_id}")
            
            # Send initial configuration
            await websocket.send(json.dumps({
                "type": "init",
                "session_id": session_id
            }))
            
            # Handle incoming messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await on_message_callback(data)
                except json.JSONDecodeError:
                    # Handle binary audio data
                    await on_message_callback({
                        "type": "audio",
                        "data": message
                    })
    
    async def analyze_speech(
        self,
        audio_data: bytes,
        analysis_type: str = "full"
    ) -> Dict[str, Any]:
        """Analyze speech for pronunciation, emotion, etc."""
        files = {"audio": ("audio.webm", audio_data, "audio/webm")}
        data = {"analysis_type": analysis_type}
        
        response = await self._client.post(
            f"{self.base_url}/analyze/speech",
            files=files,
            data=data
        )
        response.raise_for_status()
        return response.json()
    
    async def get_voice_models(self, language: Optional[str] = None) -> list# LearnFlow AI - Complete Project Files