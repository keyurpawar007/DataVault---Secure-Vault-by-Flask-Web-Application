"""
DataVault — DB Reset and Seeding Script
Drops all tables, recreates them, and seeds clean test data.
"""
import sys
import os

# Allow imports from src/
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from app import app
from extensions import db, bcrypt
from models.user import User
from models.item import Item

def reset_and_seed():
    print("[RESET] Starting database reset...")
    with app.app_context():
        # 1. Drop all tables
        print("[RESET] Dropping all existing tables...")
        db.drop_all()
        
        # 2. Recreate all tables
        print("[RESET] Recreating all tables...")
        db.create_all()
        
        # 3. Create default test user
        print("[SEED] Creating default test user: 'testuser' / 'test1234'...")
        hashed_password = bcrypt.generate_password_hash("test1234").decode("utf-8")
        test_user = User(
            username="testuser",
            password=hashed_password,
            email="testuser@datavault.ai"
        )
        db.session.add(test_user)
        db.session.flush() # Populate the user.id
        
        # 4. Create premium mock items for the cyberpunk dashboard
        print("[SEED] Seeding modern cyberpunk test items...")
        mock_items = [
            Item(
                name="Neural Core Config v1.4",
                description="Configuration files and environment parameters for the localized transformer neural core.",
                category="AI Research",
                user_id=test_user.id
            ),
            Item(
                name="Quantum Decryption Key",
                description="AES-256 decryption keys for the sub-orbital satellite telemetry stream. Keep highly secure.",
                category="Security",
                user_id=test_user.id
            ),
            Item(
                name="System Architecture Design",
                description="Flask backend framework combined with a glassmorphism high-performance premium web UI.",
                category="Development",
                user_id=test_user.id
            ),
            Item(
                name="Bio-Sensor Live Logs",
                description="Real-time cardiac and neural telemetry logs synchronized from external cybernetic implants.",
                category="Health",
                user_id=test_user.id
            )
        ]
        
        for item in mock_items:
            db.session.add(item)
            
        db.session.commit()
        print("[SUCCESS] Database reset and seeded successfully!")

if __name__ == "__main__":
    reset_and_seed()
