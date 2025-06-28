from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import engine, Base
from app.api import auth, voice, learning, websocket
from app.api.voice import tutor, language_practice, exam_prep, pronunciation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    yield
    logger.info("Shutting down...")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(voice.tutor.router, prefix="/api/voice/tutor", tags=["Voice Tutor"])
app.include_router(voice.language_practice.router, prefix="/api/voice/language", tags=["Language Practice"])
app.include_router(voice.exam_prep.router, prefix="/api/voice/exam", tags=["Exam Prep"])
app.include_router(voice.pronunciation.router, prefix="/api/voice/pronunciation", tags=["Pronunciation"])
app.include_router(learning.sessions.router, prefix="/api/learning/sessions", tags=["Learning Sessions"])
app.include_router(learning.progress.router, prefix="/api/learning/progress", tags=["Progress"])
app.include_router(learning.analytics.router, prefix="/api/learning/analytics", tags=["Analytics"])
app.include_router(websocket.voice_stream.router, prefix="/api/ws", tags=["WebSocket"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/api/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }