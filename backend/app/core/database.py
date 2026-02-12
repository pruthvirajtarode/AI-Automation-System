"""
Database Connection and Session Management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pymongo import MongoClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# PostgreSQL Setup
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB Setup
mongo_client = MongoClient(settings.MONGODB_URL)
mongodb = mongo_client[settings.MONGODB_DATABASE]

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
