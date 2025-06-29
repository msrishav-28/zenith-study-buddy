import asyncio
import json
import logging
from typing import Dict, Optional
from fastapi import WebSocket
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.omnidim.client import OmnidimClient
from app.models.learning_session import LearningSession
from app.models.voice_interaction import VoiceInteraction, InteractionType

logger = logging.getLogger(__name__)

class VoiceStreamHandler:
    """Handles WebSocket connections for voice streaming"""
    
    def __init__(self):
        self.omnidim_client = OmnidimClient()
        self.active_connections: Dict[str, WebSocket] = {}
        
    async def handle_connection(
        self,
        websocket: WebSocket,
        session_id: str,
        user_id: int
    ):
        """Handle a WebSocket connection for voice streaming"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        
        try:
            # Connect to Omnidim WebSocket
            await self.omnidim_client.connect_voice_stream(
                session_id=session_id,
                on_message_callback=lambda data: self._handle_omnidim_message(
                    websocket, session_id, user_id, data
                )
            )
            
            # Handle incoming messages from client
            while True:
                data = await websocket.receive()
                
                if data["type"] == "websocket.receive":
                    if "bytes" in data:
                        # Forward audio to Omnidim
                        await self._forward_audio_to_omnidim(session_id, data["bytes"])
                    elif "text" in data:
                        # Handle text commands
                        await self._handle_client_message(
                            websocket, session_id, user_id, json.loads(data["text"])
                        )
                elif data["type"] == "websocket.disconnect":
                    break
                    
        except Exception as e:
            logger.error(f"WebSocket error for session {session_id}: {e}")
        finally:
            if session_id in self.active_connections:
                del self.active_connections[session_id]
            await self._cleanup_session(session_id, user_id)
    
    async def _handle_omnidim_message(
        self,
        websocket: WebSocket,
        session_id: str,
        user_id: int,
        data: Dict
    ):
        """Handle messages from Omnidim"""
        try:
            if data["type"] == "audio":
                # Forward audio to client
                await websocket.send_bytes(data["data"])
                
            elif data["type"] == "transcript":
                # Save transcript and forward to client
                await self._save_interaction(
                    session_id, user_id, data["text"], data.get("speaker", "ai")
                )
                await websocket.send_json(data)
                
            elif data["type"] == "emotion":
                # Forward emotion data
                await websocket.send_json(data)
                
            elif data["type"] == "pronunciation":
                # Save and forward pronunciation score
                await self._save_pronunciation_score(
                    session_id, user_id, data["score"], data.get("feedback")
                )
                await websocket.send_json(data)
                
            else:
                # Forward other messages
                await websocket.send_json(data)
                
        except Exception as e:
            logger.error(f"Error handling Omnidim message: {e}")
    
    async def _handle_client_message(
        self,
        websocket: WebSocket,
        session_id: str,
        user_id: int,
        message: Dict
    ):
        """Handle text messages from client"""
        msg_type = message.get("type")
        
        if msg_type == "command":
            # Handle voice commands
            command = message.get("command")
            if command == "pause":
                await websocket.send_json({"type": "status", "message": "Session paused"})
            elif command == "resume":
                await websocket.send_json({"type": "status", "message": "Session resumed"})
                
        elif msg_type == "text":
            # Forward text to Omnidim for processing
            await self._forward_text_to_omnidim(session_id, message.get("content"))
    
    async def _forward_audio_to_omnidim(self, session_id: str, audio_data: bytes):
        """Forward audio data to Omnidim"""
        # This would be implemented based on Omnidim's streaming protocol
        pass
    
    async def _forward_text_to_omnidim(self, session_id: str, text: str):
        """Forward text to Omnidim"""
        # This would be implemented based on Omnidim's API
        pass
    
    async def _save_interaction(
        self,
        session_id: str,
        user_id: int,
        transcript: str,
        speaker: str
    ):
        """Save voice interaction to database"""
        db = SessionLocal()
        try:
            interaction = VoiceInteraction(
                session_id=session_id,
                user_id=user_id,
                type=InteractionType.USER_SPEECH if speaker == "user" else InteractionType.AI_RESPONSE,
                transcript=transcript
            )
            db.add(interaction)
            
            # Update session interaction count
            session = db.query(LearningSession).filter(
                LearningSession.id == session_id
            ).first()
            if session:
                session.interaction_count += 1
                
            db.commit()
        except Exception as e:
            logger.error(f"Error saving interaction: {e}")
            db.rollback()
        finally:
            db.close()
    
    async def _save_pronunciation_score(
        self,
        session_id: str,
        user_id: int,
        score: float,
        feedback: Optional[str]
    ):
        """Save pronunciation score"""
        db = SessionLocal()
        try:
            interaction = VoiceInteraction(
                session_id=session_id,
                user_id=user_id,
                type=InteractionType.PRONUNCIATION_FEEDBACK,
                pronunciation_score=score,
                transcript=feedback
            )
            db.add(interaction)
            db.commit()
        except Exception as e:
            logger.error(f"Error saving pronunciation score: {e}")
            db.rollback()
        finally:
            db.close()
    
    async def _cleanup_session(self, session_id: str, user_id: int):
        """Cleanup when session ends"""
        db = SessionLocal()
        try:
            session = db.query(LearningSession).filter(
                LearningSession.id == session_id,
                LearningSession.user_id == user_id
            ).first()
            
            if session:
                from datetime import datetime
                session.ended_at = datetime.utcnow()
                session.status = "completed"
                session.duration_seconds = int(
                    (session.ended_at - session.started_at).total_seconds()
                )
                db.commit()
        except Exception as e:
            logger.error(f"Error cleaning up session: {e}")
            db.rollback()
        finally:
            db.close()