'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { Brain, Menu, Moon, Sun, User, LogOut } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { useTheme } from 'next-themes'
import { useAuthStore } from '@/store/useAuthStore'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/Dropdown'

export function Header() {
  const { theme, setTheme } = useTheme()
  const router = useRouter()
  const { user, isAuthenticated, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center">
        <Link href="/" className="flex items-center space-x-2">
          <Brain className="h-6 w-6 text-primary" />
          <span className="font-bold text-xl">Zenith Study Buddy</span>
        </Link>

        <nav className="ml-8 hidden md:flex items-center space-x-6">
          {isAuthenticated && (
            <>
              <Link href="/dashboard" className="text-sm font-medium transition-colors hover:text-primary">
                Dashboard
              </Link>
              <Link href="/voice-tutor" className="text-sm font-medium transition-colors hover:text-primary">
                Voice Tutor
              </Link>
              <Link href="/language-practice" className="text-sm font-medium transition-colors hover:text-primary">
                Languages
              </Link>
              <Link href="/exam-prep" className="text-sm font-medium transition-colors hover:text-primary">
                Exam Prep
              </Link>
            </>
          )}
        </nav>

        <div className="ml-auto flex items-center space-x-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          >
            <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            <span className="sr-only">Toggle theme</span>
          </Button>

          {isAuthenticated ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="rounded-full">
                  <User className="h-5 w-5" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem disabled>
                  <span className="font-medium">{user?.fullName}</span>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => router.push('/profile')}>
                  Profile
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => router.push('/settings')}>
                  Settings
                </DropdownMenuItem>
                <DropdownMenuItem onClick={handleLogout}>
                  <LogOut className="mr-2 h-4 w-4" />
                  Logout
                # Complete Missing Files for Zenith Study Buddy

## Backend Files

### 1. `backend/app/api/websocket/voice_stream_handler.py`
```python
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