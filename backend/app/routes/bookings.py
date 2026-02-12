"""
Booking API Routes
Appointment scheduling endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.schemas import BookingCreate, BookingUpdate, BookingResponse
from app.models import Booking, Lead
from app.services.booking_service import get_booking_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):
    """Create appointment booking"""
    try:
        booking_service = get_booking_service()
        
        result = await booking_service.create_booking(
            db,
            booking.lead_id,
            booking.customer_id,
            booking.scheduled_time,
            booking.meeting_type,
            booking.duration_minutes
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        # Fetch the created booking
        db_booking = db.query(Booking).filter(Booking.id == result["booking_id"]).first()
        
        return db_booking
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[BookingResponse])
async def list_bookings(
    lead_id: str = Query(None),
    customer_id: str = Query(None),
    status: str = Query(None),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    """List bookings with optional filtering"""
    try:
        query = db.query(Booking)
        
        if lead_id:
            query = query.filter(Booking.lead_id == lead_id)
        if customer_id:
            query = query.filter(Booking.customer_id == customer_id)
        if status:
            query = query.filter(Booking.status == status)
        
        bookings = query.order_by(Booking.scheduled_time).limit(limit).all()
        
        return bookings
    except Exception as e:
        logger.error(f"Error listing bookings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: str,
    db: Session = Depends(get_db)
):
    """Get specific booking details"""
    try:
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        return booking
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting booking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking(
    booking_id: str,
    booking_update: BookingUpdate,
    db: Session = Depends(get_db)
):
    """Update booking details"""
    try:
        booking_service = get_booking_service()
        
        update_data = booking_update.dict(exclude_unset=True)
        
        result = await booking_service.update_booking(db, booking_id, **update_data)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
        
        return db_booking
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating booking: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{booking_id}")
async def cancel_booking(
    booking_id: str,
    db: Session = Depends(get_db)
):
    """Cancel booking"""
    try:
        booking_service = get_booking_service()
        
        result = await booking_service.cancel_booking(db, booking_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling booking: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/availability/check")
async def check_availability(
    date_time: str,  # ISO format
    duration_minutes: int = 30,
    db: Session = Depends(get_db)
):
    """Check availability for time slot"""
    try:
        booking_service = get_booking_service()
        
        scheduled_time = datetime.fromisoformat(date_time)
        
        availability = await booking_service.check_availability(
            scheduled_time,
            duration_minutes
        )
        
        return availability
    except Exception as e:
        logger.error(f"Error checking availability: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
