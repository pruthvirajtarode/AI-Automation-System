"""
Message API Routes
Handles incoming messages and AI responses
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import MessageCreate, MessageResponse, AIResponseRequest
from app.models import Message, Customer
from app.services.ai_service import get_ai_service
from app.services.crm_service import get_crm_service
from app.services.message_channel import ChannelFactory
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/receive", response_model=MessageResponse)
async def receive_message(
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    """
    Receive incoming message from customer
    
    Supports multiple channels: SMS, Email, Chat, Forms
    """
    try:
        # Get or create customer
        customer = db.query(Customer).filter(
            Customer.email == message.customer_id
        ).first()
        
        if not customer:
            # Create new customer (basic info)
            customer = Customer(
                email=message.customer_id,
                name="New Customer",
                phone="Pending"
            )
            db.add(customer)
            db.commit()
        
        # Save message to database
        crm_service = get_crm_service()
        save_result = await crm_service.save_customer_interaction(
            db,
            customer.id,
            message.content,
            message.channel,
            message.direction
        )
        
        if not save_result.get("success"):
            raise HTTPException(status_code=400, detail="Failed to save message")
        
        # Generate AI response
        ai_service = get_ai_service()
        ai_result = await ai_service.process_message(
            message.content,
            context={
                "company": customer.company,
                "name": customer.name
            }
        )
        
        # Update message with AI response
        msg = db.query(Message).filter(Message.id == save_result["message_id"]).first()
        if msg:
            msg.ai_response = ai_result.get("response")
            msg.processed = True
            db.commit()
        
        # Send AI response back to customer
        if ai_result.get("success"):
            await ChannelFactory.send_message(
                channel=message.channel,
                recipient=customer.email if message.channel == "email" else customer.phone,
                content=ai_result.get("response")
            )
        
        return MessageResponse(
            id=save_result["message_id"],
            customer_id=customer.id,
            channel=message.channel,
            direction=message.direction,
            content=message.content,
            ai_response=ai_result.get("response"),
            processed=True,
            created_at=msg.created_at if msg else None
        )
    
    except Exception as e:
        logger.error(f"Error receiving message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai-response")
async def generate_ai_response(
    request: AIResponseRequest
):
    """
    Generate AI response to customer message
    """
    try:
        ai_service = get_ai_service()
        
        result = await ai_service.process_message(
            request.customer_message,
            context=request.customer_context
        )
        
        return result
    except Exception as e:
        logger.error(f"Error generating AI response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[MessageResponse])
async def list_messages(
    customer_id: str = Query(None),
    channel: str = Query(None),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    """
    List messages with optional filtering
    """
    try:
        query = db.query(Message)
        
        if customer_id:
            query = query.filter(Message.customer_id == customer_id)
        
        if channel:
            query = query.filter(Message.channel == channel)
        
        messages = query.order_by(Message.created_at.desc()).limit(limit).all()
        
        return messages
    except Exception as e:
        logger.error(f"Error listing messages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: str,
    db: Session = Depends(get_db)
):
    """
    Get specific message details
    """
    try:
        message = db.query(Message).filter(Message.id == message_id).first()
        
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        return message
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send/{channel}")
async def send_message(
    channel: str,
    recipient: str,
    content: str,
    db: Session = Depends(get_db)
):
    """
    Send message through specified channel
    """
    try:
        result = await ChannelFactory.send_message(
            channel=channel,
            recipient=recipient,
            content=content
        )
        
        if result.get("success"):
            # Save outbound message to database
            customer = db.query(Customer).filter(
                Customer.email == recipient
            ).first()
            
            if customer:
                message = Message(
                    customer_id=customer.id,
                    channel=channel,
                    direction="outbound",
                    content=content,
                    ai_response=content,
                    processed=True
                )
                db.add(message)
                db.commit()
        
        return result
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
