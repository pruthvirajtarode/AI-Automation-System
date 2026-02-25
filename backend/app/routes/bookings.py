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
from app.models import Booking, Lead, Customer
from app.services.booking_service import get_booking_service
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter()


def _booking_with_customer(booking, db):
    """Build booking response with customer_name"""
    customer_name = None
    if booking.customer_id:
        customer = db.query(Customer).filter(Customer.id == booking.customer_id).first()
        if customer:
            customer_name = customer.name
    return {
        "id": booking.id,
        "lead_id": booking.lead_id,
        "customer_id": booking.customer_id,
        "customer_name": customer_name,
        "scheduled_time": booking.scheduled_time,
        "meeting_type": booking.meeting_type,
        "duration_minutes": booking.duration_minutes,
        "status": booking.status,
        "meeting_link": booking.meeting_link,
        "notes": booking.notes if hasattr(booking, 'notes') else None,
        "created_at": booking.created_at,
    }


@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):
    """Create appointment booking"""
    try:
        # Direct DB creation for flexibility (lead_id/customer_id are optional)
        db_booking = Booking(
            id=str(uuid.uuid4()),
            lead_id=booking.lead_id,
            customer_id=booking.customer_id,
            scheduled_time=booking.scheduled_time,
            meeting_type=booking.meeting_type or "consultation",
            duration_minutes=booking.duration_minutes or 30,
            meeting_link=booking.meeting_link,
            notes=booking.notes,
            status="scheduled",
        )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)

        return _booking_with_customer(db_booking, db)
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
    """List bookings with customer names"""
    try:
        query = db.query(Booking)
        
        if lead_id:
            query = query.filter(Booking.lead_id == lead_id)
        if customer_id:
            query = query.filter(Booking.customer_id == customer_id)
        if status:
            query = query.filter(Booking.status == status)
        
        bookings = query.order_by(Booking.scheduled_time).limit(limit).all()

        return [_booking_with_customer(b, db) for b in bookings]
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
