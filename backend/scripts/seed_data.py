#!/usr/bin/env python3
"""Seed the database with sample data"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
import random
from app.database import SessionLocal
from app.models.user import User, LearningStyle
from app.models.learning_session import LearningSession, SessionType
from app.models.progress import Progress, Achievement
from app.core.security import get_password_hash

def seed_users(db):
    """Create sample users"""
    users_data = [
        {
            "username": "demo_student",
            "email": "demo@zenithstudy.com",
            "full_name": "Demo Student",
            "learning_style": LearningStyle.VISUAL,
            "preferred_language": "en-US"
        },
        {
            "username": "john_doe",
            "email": "john@example.com",
            "full_name": "John Doe",
            "learning_style": LearningStyle.AUDITORY,
            "preferred_language": "en-US"
        }
    ]
    
    created_users = []
    for user_data in users_data:
        user = db.query(User).filter(User.username == user_data["username"]).first()
        if not user:
            user = User(
                **user_data,
                hashed_password=get_password_hash("Demo123!")
            )
            db.add(user)
            created_users.append(user)
    
    db.commit()
    return created_users

def seed_learning_sessions(db, users):
    """Create sample learning sessions"""
    subjects = ["mathematics", "physics", "chemistry", "programming", "languages"]
    
    for user in users:
        # Create 10-20 sessions per user
        for i in range(random.randint(10, 20)):
            session = LearningSession(
                user_id=user.id,
                omnidim_session_id=f"omnidim_{user.id}_{i}",
                type=random.choice(list(SessionType)),
                subject=random.choice(subjects),
                difficulty=random.choice(["beginner", "intermediate", "advanced"]),
                started_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                duration_seconds=random.randint(600, 3600),
                interaction_count=random.randint(5, 50),
                comprehension_score=random.uniform(0.6, 0.95),
                pronunciation_score=random.uniform(0.7, 0.98),
                status="completed"
            )
            session.ended_at = session.started_at + timedelta(seconds=session.duration_seconds)
            db.add(session)
    
    db.commit()

def seed_progress(db, users):
    """Create progress records"""
    for user in users:
        progress = Progress(
            user_id=user.id,
            total_study_time=random.randint(10000, 50000),
            total_sessions=random.randint(20, 100),
            current_streak=random.randint(1, 30),
            longest_streak=random.randint(30, 90),
            level=random.randint(1, 10),
            experience_points=random.randint(100, 5000),
            overall_accuracy=random.uniform(0.7, 0.95)
        )
        db.add(progress)
    
    db.commit()

def seed_achievements(db, users):
    """Create sample achievements"""
    achievements_list = [
        ("First Steps", "Complete your first learning session", "🎯"),
        ("Week Warrior", "Study for 7 days in a row", "🔥"),
        ("Knowledge Seeker", "Complete 50 sessions", "📚"),
        ("Pronunciation Pro", "Achieve 90% pronunciation score", "🗣️"),
        ("Speed Learner", "Complete 5 sessions in one day", "⚡")
    ]
    
    for user in users:
        # Give each user 2-4 achievements
        num_achievements = random.randint(2, 4)
        selected = random.sample(achievements_list, num_achievements)
        
        for name, desc, icon in selected:
            achievement = Achievement(
                user_id=user.id,
                name=name,
                description=desc,
                icon=icon,
                category="general",
                progress_value=100,
                progress_max=100
            )
            db.add(achievement)
    
    db.commit()

def main():
    """Run all seeders"""
    db = SessionLocal()
    
    try:
        print("Seeding users...")
        users = seed_users(db)
        
        print("Seeding learning sessions...")
        seed_learning_sessions(db, users)
        
        print("Seeding progress...")
        seed_progress(db, users)
        
        print("Seeding achievements...")
        seed_achievements(db, users)
        
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()