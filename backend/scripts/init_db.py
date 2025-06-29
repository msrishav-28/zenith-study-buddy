#!/usr/bin/env python3
"""Initialize the database with tables and initial data"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from app.database import Base, SessionLocal
from app.config import settings
from app.models import user, learning_session, voice_interaction, progress

def init_db():
    """Initialize database"""
    print("Creating database tables...")
    
    # Create engine
    engine = create_engine(settings.DATABASE_URL)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("Database tables created successfully!")
    
    # Create default data
    db = SessionLocal()
    try:
        # Check if we need to create admin user
        from app.models.user import User
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            from app.core.security import get_password_hash
            admin = User(
                username="admin",
                email="admin@zenithstudy.com",
                full_name="Admin User",
                hashed_password=get_password_hash("admin123!"),
                is_active=True,
                is_premium=True,
                is_verified=True
            )
            db.add(admin)
            db.commit()
            print("Admin user created!")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()