"""
DataVault — DB Migration Script
Adds new columns to existing tables without dropping data.
"""
import sys
sys.path.insert(0, "src")

from app import app
from extensions import db
from sqlalchemy import text

migrations = [
    ("users",  "email",      "VARCHAR(150) NULL"),
    ("users",  "created_at", "DATETIME NULL"),
    ("items",  "category",   "VARCHAR(80) NULL DEFAULT 'General'"),
    ("items",  "created_at", "DATETIME NULL"),
    ("items",  "updated_at", "DATETIME NULL"),
    ("items",  "user_id",    "INTEGER NULL"),
]

with app.app_context():
    with db.engine.connect() as conn:
        for table, col, definition in migrations:
            try:
                sql = f"ALTER TABLE {table} ADD COLUMN {col} {definition}"
                conn.execute(text(sql))
                conn.commit()
                print(f"[OK] Added {table}.{col}")
            except Exception as e:
                err = str(e)
                if "Duplicate column" in err or "1060" in err:
                    print(f"[SKIP] {table}.{col} already exists")
                else:
                    print(f"[ERR] {table}.{col}: {e}")

    print("\nMigration complete!")
