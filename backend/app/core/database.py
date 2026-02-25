"""
Database Connection and Session Management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
import logging
import os

logger = logging.getLogger(__name__)

# PostgreSQL / SQLite Setup
db_url = settings.DATABASE_URL

# Fallback to SQLite for local development if PostgreSQL is unavailable
if db_url.startswith("postgresql"):
    try:
        _test_engine = create_engine(db_url, pool_pre_ping=True)
        with _test_engine.connect() as conn:
            pass
        engine = _test_engine
        logger.info("Connected to PostgreSQL")
    except Exception as e:
        logger.warning(f"PostgreSQL unavailable ({e}), falling back to SQLite")
        db_url = "sqlite:///./local_dev.db"
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(db_url, pool_pre_ping=True, echo=settings.DEBUG)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB Setup (optional - graceful fallback)
mongodb = None
try:
    from pymongo import MongoClient
    mongo_client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=3000)
    mongo_client.admin.command('ping')
    mongodb = mongo_client[settings.MONGODB_DATABASE]
    logger.info("Connected to MongoDB")
except Exception as e:
    logger.warning(f"MongoDB unavailable ({e}), running without MongoDB")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")

def get_mongodb():
    """Get MongoDB database"""
    return mongodb
