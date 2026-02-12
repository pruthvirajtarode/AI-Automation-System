"""
Follow-up API Routes
Automated follow-up and engagement endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.schemas import FollowUpCreate, FollowUpResponse
from app.models import FollowUp
from app.services.follow_up_service import get_follow_up_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=FollowUpResponse)
async def schedule_follow_up(
    follow_up: FollowUpCreate,
    db: Session = Depends(get_db)
):
    """Schedule follow-up message"""
    try:
        follow_up_service = get_follow_up_service()
        
        result = await follow_up_service.schedule_follow_up(
            db,
            follow_up.lead_id,
            follow_up.message_type,
            follow_up.scheduled_time,
            follow_up.message_content
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        # Fetch the created follow-up
        fu = db.query(FollowUp).filter(FollowUp.id == result["follow_up_id"]).first()
        
        return fu
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error scheduling follow-up: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[FollowUpResponse])
async def list_follow_ups(
    lead_id: str = Query(None),
    message_type: str = Query(None),
    sent: bool = Query(None),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    """List follow-ups with optional filtering"""
    try:
        query = db.query(FollowUp)
        
        if lead_id:
            query = query.filter(FollowUp.lead_id == lead_id)
        if message_type:
            query = query.filter(FollowUp.message_type == message_type)
        if sent is not None:
            query = query.filter(FollowUp.sent == sent)
        
        follow_ups = query.order_by(FollowUp.scheduled_time).limit(limit).all()
        
        return follow_ups
    except Exception as e:
        logger.error(f"Error listing follow-ups: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{follow_up_id}", response_model=FollowUpResponse)
async def get_follow_up(
    follow_up_id: str,
    db: Session = Depends(get_db)
):
    """Get specific follow-up details"""
    try:
        follow_up = db.query(FollowUp).filter(FollowUp.id == follow_up_id).first()
        
        if not follow_up:
            raise HTTPException(status_code=404, detail="Follow-up not found")
        
        return follow_up
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting follow-up: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{lead_id}/sequence/{sequence_type}")
async def create_follow_up_sequence(
    lead_id: str,
    sequence_type: str,
    db: Session = Depends(get_db)
):
    """Create automated follow-up sequence"""
    try:
        follow_up_service = get_follow_up_service()
        
        result = await follow_up_service.create_follow_up_sequence(
            db,
            lead_id,
            sequence_type
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating follow-up sequence: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send/pending")
async def send_pending_follow_ups(
    db: Session = Depends(get_db)
):
    """Send all pending follow-ups that are due"""
    try:
        follow_up_service = get_follow_up_service()
        
        result = await follow_up_service.send_pending_follow_ups(db)
        
        return result
    except Exception as e:
        logger.error(f"Error sending follow-ups: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{follow_up_id}")
async def cancel_follow_up(
    follow_up_id: str,
    db: Session = Depends(get_db)
):
    """Cancel follow-up"""
    try:
        follow_up = db.query(FollowUp).filter(FollowUp.id == follow_up_id).first()
        
        if not follow_up:
            raise HTTPException(status_code=404, detail="Follow-up not found")
        
        db.delete(follow_up)
        db.commit()
        
        return {"status": "cancelled", "follow_up_id": follow_up_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling follow-up: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
