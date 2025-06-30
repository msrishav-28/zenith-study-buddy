#!/usr/bin/env python3
"""Initialize SQLite database - no installation needed!"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from app.database import Base
from app.config import settings
from app.models import user, learning_session, voice_interaction, progress
from app.core.security import get_password_hash
from app.database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize SQLite database"""
    logger.info("🚀 Initializing SQLite database...")
    
    # Create database file and tables
    try:
        engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created!")
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        return False
    
    # Create default users
    db = SessionLocal()
    try:
        from app.models.user import User, LearningStyle
        
        # Admin user
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@zenithstudy.com",
                full_name="Admin User",
                hashed_password=get_password_hash("Admin123!"),
                is_active=True,
                is_premium=True,
                is_verified=True
            )
            db.add(admin)
            logger.info("✅ Admin user created!")
        
        # Demo user
        demo = db.query(User).filter(User.username == "demo_student").first()
        if not demo:
            demo = User(
                username="demo_student",
                email="demo@zenithstudy.com",
                full_name="Demo Student",
                hashed_password=get_password_hash("Demo123!"),
                learning_style=LearningStyle.VISUAL,
                preferred_language="en-US",
                is_active=True,
                is_premium=False,
                is_verified=True
            )
            db.add(demo)
            logger.info("✅ Demo user created!")
        
        db.commit()
        logger.info("\n✅ SQLite database ready!")
        logger.info("📁 Database file: zenith_study_buddy.db")
        logger.info("\n📋 Login credentials:")
        logger.info("   Admin: admin / Admin123!")
        logger.info("   Demo: demo_student / Demo123!")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating users: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    if not init_database():
        sys.exit(1)