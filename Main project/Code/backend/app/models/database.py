"""
Database Configuration and Session Management

This module sets up SQLAlchemy database connection and session management
for PostgreSQL database.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment variables
# Use SQLite for easier setup (no external database required)
# For production, switch to PostgreSQL by setting DATABASE_URL env var
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./asl_narration.db"  # SQLite - works out of the box
)

# Convert to psycopg3 format if using PostgreSQL
if DATABASE_URL.startswith("postgresql://"):
    try:
        import psycopg
        # Use psycopg3 driver
        if "+psycopg" not in DATABASE_URL:
            DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
    except ImportError:
        # Fall back to psycopg2 if psycopg3 not available
        pass

# Create SQLAlchemy engine
# SQLite doesn't support pool_size, so adjust based on database type
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # SQLite specific
        echo=False
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=10,
        max_overflow=20
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for database models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Used in FastAPI route handlers via Depends().
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

