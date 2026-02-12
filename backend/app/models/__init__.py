"""
Database Models
ORM models for SQLAlchemy
"""

from sqlalchemy import Column, String, DateTime, Boolean, Float, Integer, Text, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import uuid
import enum

class LeadStatus(str, enum.Enum):
    """Lead status enumeration"""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    IN_NEGOTIATION = "in_negotiation"
    WON = "won"
    LOST = "lost"

class MessageChannel(str, enum.Enum):
    """Message channel enumeration"""
    SMS = "sms"
    EMAIL = "email"
    CHAT = "chat"
    FORM = "form"
    SOCIAL = "social"

class TaskStatus(str, enum.Enum):
    """Task status enumeration"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLOSED = "closed"

class Customer(Base):
    """Customer model"""
    __tablename__ = "customers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20), unique=True, index=True)
    company = Column(String(255))
    business_type = Column(String(100))
    location = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = relationship("Message", back_populates="customer")
    leads = relationship("Lead", back_populates="customer")

class Lead(Base):
    """Lead model"""
    __tablename__ = "leads"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW, index=True)
    quality_score = Column(Float, default=0.0)
    requirements = Column(Text)
    timeline = Column(String(100))
    budget = Column(String(100))
    priority = Column(String(20))  # high, medium, low
    notes = Column(Text)
    assigned_to = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="leads")
    tasks = relationship("Task", back_populates="lead")

class Message(Base):
    """Message model"""
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    channel = Column(Enum(MessageChannel), nullable=False, index=True)
    direction = Column(String(20))  # inbound or outbound
    content = Column(Text, nullable=False)
    ai_response = Column(Text)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="messages")

class Task(Base):
    """Task model"""
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String, ForeignKey("leads.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.OPEN, index=True)
    assigned_to = Column(String(255))
    task_type = Column(String(50))  # sales, support, technical
    priority = Column(String(20))  # high, medium, low
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="tasks")

class Booking(Base):
    """Appointment Booking model"""
    __tablename__ = "bookings"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String, ForeignKey("leads.id"), nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=30)
    meeting_type = Column(String(100))  # call, demo, consultation
    meeting_link = Column(String(255))
    status = Column(String(20))  # scheduled, completed, cancelled
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class FollowUp(Base):
    """Follow-up Automation model"""
    __tablename__ = "follow_ups"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String, ForeignKey("leads.id"), nullable=False)
    message_type = Column(String(50))  # reminder, nurture, check_in
    scheduled_time = Column(DateTime, nullable=False)
    message_content = Column(Text)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime)
