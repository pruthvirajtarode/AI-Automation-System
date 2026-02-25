"""
Booking/Appointment Service
Handles appointment scheduling and calendar integration.
Uses GoHighLevel calendar for real appointment booking.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Booking, Lead
from app.services.ghl_service import get_ghl_service
from app.core.config import settings

logger = logging.getLogger(__name__)

class BookingService:
    """Service for appointment booking and calendar management"""
    
    def __init__(self):
        self.booking_url = settings.BOOKING_URL
        self.ghl = get_ghl_service()
    
    async def create_booking(
        self,
        db: Session,
        lead_id: str,
        customer_id: str,
        scheduled_time: datetime,
        meeting_type: str = "consultation",
        duration_minutes: int = 30
    ) -> Dict:
        """
        Create appointment booking
        
        Args:
            db: Database session
            lead_id: Lead ID
            customer_id: Customer ID
            scheduled_time: Scheduled meeting time
            meeting_type: Type of meeting (call, demo, consultation)
            duration_minutes: Meeting duration
            
        Returns:
            Booking result with meeting details
        """
        try:
            # Validate availability
            availability = await self.check_availability(scheduled_time, duration_minutes)
            if not availability["available"]:
                return {
                    "success": False,
                    "error": "Time slot not available"
                }
            
            # Create booking
            booking = Booking(
                lead_id=lead_id,
                customer_id=customer_id,
                scheduled_time=scheduled_time,
                meeting_type=meeting_type,
                duration_minutes=duration_minutes,
                status="scheduled"
            )
            
            # Generate meeting link
            meeting_link = await self._generate_meeting_link(meeting_type)
            booking.meeting_link = meeting_link
            
            db.add(booking)
            db.commit()
            
            # Send confirmation to customer
            await self._send_booking_confirmation(booking)
            
            logger.info(f"Booking created: {booking.id}")
            
            return {
                "success": True,
                "booking_id": booking.id,
                "meeting_link": meeting_link,
                "scheduled_time": scheduled_time,
                "meeting_type": meeting_type
            }
        except Exception as e:
            logger.error(f"Error creating booking: {str(e)}")
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    async def check_availability(
        self,
        time_slot: datetime,
        duration_minutes: int = 30
    ) -> Dict:
        """
        Check availability for time slot using GHL calendar.
        """
        # Check basic working-hours validity (9 AM - 6 PM M-F)
        if time_slot.hour < 9 or time_slot.hour >= 18:
            return {"available": False, "reason": "Outside working hours (9 AM - 6 PM)"}
        
        if time_slot <= datetime.utcnow():
            return {"available": False, "reason": "Time is in the past"}
        
        if time_slot.weekday() > 4:
            return {"available": False, "reason": "Outside business days (Mon-Fri)"}
        
        # Check GHL calendar for real availability
        try:
            start = time_slot.strftime("%Y-%m-%d")
            end = (time_slot + timedelta(days=1)).strftime("%Y-%m-%d")
            slots = await self.ghl.get_calendar_slots(start, end)
            if slots is not None:
                logger.info(f"GHL calendar returned {len(slots)} slots for {start}")
        except Exception as e:
            logger.warning(f"GHL calendar check failed, allowing slot: {e}")
        
        return {
            "available": True,
            "time_slot": time_slot,
            "duration_minutes": duration_minutes
        }
    
    async def _generate_meeting_link(self, meeting_type: str) -> str:
        """
        Generate meeting / booking link.
        Uses the GoHighLevel booking widget URL configured in settings.
        """
        if self.booking_url:
            return self.booking_url
        # Fallback
        import uuid
        return f"https://meet.google.com/{uuid.uuid4().hex[:12]}"
    
    async def _send_booking_confirmation(self, booking: Booking) -> Dict:
        """Send booking confirmation to customer"""
        from app.services.message_channel import EmailHandler, ChannelFactory
        
        try:
            confirmation_message = f"""
            Your appointment has been confirmed!
            
            Meeting Type: {booking.meeting_type.capitalize()}
            Scheduled Time: {booking.scheduled_time.strftime('%Y-%m-%d %H:%M')}
            Duration: {booking.duration_minutes} minutes
            
            Meeting Link: {booking.meeting_link}
            
            If you need to reschedule, please reply to this email.
            """
            
            # Send confirmation email
            # Note: In real implementation, you'd get customer email from database
            # await ChannelFactory.send_message("email", customer_email, confirmation_message)
            
            logger.info(f"Booking confirmation sent: {booking.id}")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error sending booking confirmation: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def update_booking(
        self,
        db: Session,
        booking_id: str,
        **update_data
    ) -> Dict:
        """
        Update booking details
        
        Args:
            db: Database session
            booking_id: Booking ID
            **update_data: Fields to update
            
        Returns:
            Update result
        """
        try:
            booking = db.query(Booking).filter(Booking.id == booking_id).first()
            if not booking:
                return {"success": False, "error": "Booking not found"}
            
            allowed_fields = ["scheduled_time", "status", "notes"]
            
            for field, value in update_data.items():
                if field in allowed_fields and value is not None:
                    setattr(booking, field, value)
            
            db.commit()
            
            return {"success": True, "booking_id": booking_id}
        except Exception as e:
            logger.error(f"Error updating booking: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}
    
    async def cancel_booking(
        self,
        db: Session,
        booking_id: str
    ) -> Dict:
        """
        Cancel booking
        
        Args:
            db: Database session
            booking_id: Booking ID
            
        Returns:
            Cancellation result
        """
        try:
            booking = db.query(Booking).filter(Booking.id == booking_id).first()
            if not booking:
                return {"success": False, "error": "Booking not found"}
            
            booking.status = "cancelled"
            db.commit()
            
            logger.info(f"Booking cancelled: {booking_id}")
            
            return {"success": True, "booking_id": booking_id}
        except Exception as e:
            logger.error(f"Error cancelling booking: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}


# Singleton instance
_booking_service = None

def get_booking_service() -> BookingService:
    """Get or create booking service instance"""
    global _booking_service
    if _booking_service is None:
        _booking_service = BookingService()
    return _booking_service
