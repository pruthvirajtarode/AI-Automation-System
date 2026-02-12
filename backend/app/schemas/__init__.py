"""
Pydantic Schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Customer Schemas
class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    company: Optional[str] = None
    business_type: Optional[str] = None
    location: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    business_type: Optional[str] = None
    location: Optional[str] = None

class CustomerResponse(CustomerBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Lead Schemas
class LeadBase(BaseModel):
    status: Optional[str] = "new"
    quality_score: Optional[float] = 0.0
    requirements: Optional[str] = None
    timeline: Optional[str] = None
    budget: Optional[str] = None

class LeadCreate(LeadBase):
    customer_id: str

class LeadUpdate(BaseModel):
    status: Optional[str] = None
    quality_score: Optional[float] = None
    requirements: Optional[str] = None
    timeline: Optional[str] = None
    budget: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None

class LeadResponse(LeadBase):
    id: str
    customer_id: str
    priority: Optional[str]
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Message Schemas
class MessageBase(BaseModel):
    channel: str
    content: str

class MessageCreate(MessageBase):
    customer_id: str
    direction: str = "inbound"

class MessageResponse(MessageBase):
    id: str
    customer_id: str
    direction: str
    ai_response: Optional[str] = None
    processed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: str

class TaskCreate(TaskBase):
    lead_id: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    priority: Optional[str] = None

class TaskResponse(TaskBase):
    id: str
    lead_id: str
    status: str
    assigned_to: Optional[str]
    priority: Optional[str]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Booking Schemas
class BookingCreate(BaseModel):
    lead_id: str
    customer_id: str
    scheduled_time: datetime
    meeting_type: str
    duration_minutes: Optional[int] = 30
    notes: Optional[str] = None

class BookingUpdate(BaseModel):
    scheduled_time: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class BookingResponse(BaseModel):
    id: str
    lead_id: str
    customer_id: str
    scheduled_time: datetime
    meeting_type: str
    status: str
    meeting_link: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Follow-up Schemas
class FollowUpCreate(BaseModel):
    lead_id: str
    message_type: str
    scheduled_time: datetime
    message_content: str

class FollowUpResponse(BaseModel):
    id: str
    lead_id: str
    message_type: str
    scheduled_time: datetime
    message_content: str
    sent: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# AI Response Schemas
class LeadQualificationRequest(BaseModel):
    customer_id: str
    message_content: str

class LeadQualificationResponse(BaseModel):
    quality_score: float
    priority: str
    recommendations: List[str]
    next_actions: List[str]

class AIResponseRequest(BaseModel):
    customer_message: str
    conversation_history: Optional[List[dict]] = None
    customer_context: Optional[dict] = None
