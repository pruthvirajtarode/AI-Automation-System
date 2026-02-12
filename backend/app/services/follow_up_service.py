"""
Follow-up Automation Service
Manages automated follow-ups and reminders
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import FollowUp, Lead
from app.services.ai_service import get_ai_service
from app.services.message_channel import ChannelFactory

logger = logging.getLogger(__name__)

class FollowUpService:
    """Service for automated follow-ups and engagement"""
    
    def __init__(self):
        self.follow_up_sequences = {
            "nurture": {
                "day_1": "Thank you for your interest!",
                "day_3": "Here are some resources that might help...",
                "day_7": "Still interested? Let's schedule a call.",
                "day_14": "Final reminder about our services"
            },
            "reminder": {
                "hour_1": "Quick reminder about your inquiry",
                "day_1": "Following up on your request"
            },
            "post_demo": {
                "hour_24": "Thank you for attending the demo!",
                "day_3": "Questions about the demo?",
                "day_7": "Ready to move forward?"
            }
        }
    
    async def schedule_follow_up(
        self,
        db: Session,
        lead_id: str,
        follow_up_type: str,
        scheduled_time: datetime,
        message_content: Optional[str] = None
    ) -> Dict:
        """
        Schedule automated follow-up
        
        Args:
            db: Database session
            lead_id: Lead ID
            follow_up_type: Type of follow-up (reminder, nurture, check_in)
            scheduled_time: When to send follow-up
            message_content: Custom message content
            
        Returns:
            Follow-up scheduling result
        """
        try:
            # Generate message if not provided
            if not message_content:
                message_content = await self._generate_follow_up_message(
                    db, lead_id, follow_up_type
                )
            
            # Create follow-up record
            follow_up = FollowUp(
                lead_id=lead_id,
                message_type=follow_up_type,
                scheduled_time=scheduled_time,
                message_content=message_content,
                sent=False
            )
            
            db.add(follow_up)
            db.commit()
            
            logger.info(f"Follow-up scheduled: {follow_up.id}")
            
            return {
                "success": True,
                "follow_up_id": follow_up.id,
                "scheduled_time": scheduled_time,
                "type": follow_up_type
            }
        except Exception as e:
            logger.error(f"Error scheduling follow-up: {str(e)}")
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_follow_up_sequence(
        self,
        db: Session,
        lead_id: str,
        sequence_type: str
    ) -> Dict:
        """
        Create automated follow-up sequence
        
        Args:
            db: Database session
            lead_id: Lead ID
            sequence_type: Type of sequence (nurture, reminder, post_demo)
            
        Returns:
            Sequence creation result
        """
        try:
            sequence = self.follow_up_sequences.get(sequence_type)
            if not sequence:
                return {
                    "success": False,
                    "error": f"Unknown sequence type: {sequence_type}"
                }
            
            # Create follow-ups for each step in sequence
            follow_ups = []
            base_time = datetime.utcnow()
            
            for step, message in sequence.items():
                # Parse timing from step name
                scheduled_time = self._parse_timing(step, base_time)
                
                follow_up = FollowUp(
                    lead_id=lead_id,
                    message_type=sequence_type,
                    scheduled_time=scheduled_time,
                    message_content=message,
                    sent=False
                )
                
                db.add(follow_up)
                follow_ups.append(follow_up)
            
            db.commit()
            
            logger.info(f"Follow-up sequence created: {len(follow_ups)} messages")
            
            return {
                "success": True,
                "sequence_type": sequence_type,
                "follow_ups_created": len(follow_ups)
            }
        except Exception as e:
            logger.error(f"Error creating follow-up sequence: {str(e)}")
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_pending_follow_ups(self, db: Session) -> Dict:
        """
        Send all pending follow-ups that are due
        
        Args:
            db: Database session
            
        Returns:
            Send result with count of sent messages
        """
        try:
            now = datetime.utcnow()
            
            # Get pending follow-ups
            pending = db.query(FollowUp).filter(
                (FollowUp.sent == False) &
                (FollowUp.scheduled_time <= now)
            ).all()
            
            sent_count = 0
            failed_count = 0
            
            for follow_up in pending:
                # Get lead and customer info
                lead = db.query(Lead).filter(Lead.id == follow_up.lead_id).first()
                if not lead:
                    continue
                
                # Send follow-up through appropriate channel
                # TODO: Determine preferred channel from customer preferences
                send_result = await ChannelFactory.send_message(
                    channel="email",
                    recipient=lead.customer.email,
                    content=follow_up.message_content,
                    subject=f"Follow-up: {follow_up.message_type}"
                )
                
                if send_result.get("success"):
                    follow_up.sent = True
                    follow_up.sent_at = now
                    sent_count += 1
                else:
                    failed_count += 1
            
            db.commit()
            
            logger.info(f"Follow-ups sent: {sent_count}, Failed: {failed_count}")
            
            return {
                "success": True,
                "sent": sent_count,
                "failed": failed_count
            }
        except Exception as e:
            logger.error(f"Error sending follow-ups: {str(e)}")
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _generate_follow_up_message(
        self,
        db: Session,
        lead_id: str,
        follow_up_type: str
    ) -> str:
        """
        Generate personalized follow-up message using AI
        
        Args:
            db: Database session
            lead_id: Lead ID
            follow_up_type: Type of follow-up
            
        Returns:
            Generated message
        """
        try:
            lead = db.query(Lead).filter(Lead.id == lead_id).first()
            if not lead:
                return "Following up on your inquiry. How can we help?"
            
            ai_service = get_ai_service()
            lead_data = {
                "name": lead.customer.name,
                "company": lead.customer.company,
                "last_interaction": "Recent inquiry"
            }
            
            message = await ai_service.generate_follow_up(lead_data, follow_up_type)
            return message
        except Exception as e:
            logger.error(f"Error generating follow-up message: {str(e)}")
            return "Following up on your inquiry. How can we help?"
    
    def _parse_timing(self, step: str, base_time: datetime) -> datetime:
        """
        Parse timing from step name
        
        Args:
            step: Step identifier (e.g., 'day_1', 'hour_24')
            base_time: Base time to calculate from
            
        Returns:
            Calculated datetime
        """
        if step.startswith("hour_"):
            hours = int(step.split("_")[1])
            return base_time + timedelta(hours=hours)
        elif step.startswith("day_"):
            days = int(step.split("_")[1])
            return base_time + timedelta(days=days)
        else:
            return base_time + timedelta(days=1)


# Singleton instance
_follow_up_service = None

def get_follow_up_service() -> FollowUpService:
    """Get or create follow-up service instance"""
    global _follow_up_service
    if _follow_up_service is None:
        _follow_up_service = FollowUpService()
    return _follow_up_service
