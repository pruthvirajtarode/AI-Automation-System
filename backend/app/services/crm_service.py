"""
CRM Integration Service
Handles CRM updates and customer data synchronization
"""

import logging
from typing import Dict, Optional
from sqlalchemy.orm import Session
from app.models import Lead, Customer, Message
from datetime import datetime

logger = logging.getLogger(__name__)

class CRMService:
    """Service for CRM operations and integrations"""
    
    async def save_customer_interaction(
        self,
        db: Session,
        customer_id: str,
        message_content: str,
        channel: str,
        direction: str = "inbound"
    ) -> Dict:
        """
        Save customer interaction to CRM
        
        Args:
            db: Database session
            customer_id: Customer ID
            message_content: Message content
            channel: Communication channel
            direction: Message direction (inbound/outbound)
            
        Returns:
            Save result
        """
        try:
            message = Message(
                customer_id=customer_id,
                channel=channel,
                direction=direction,
                content=message_content,
                processed=False
            )
            
            db.add(message)
            db.commit()
            
            logger.info(f"Message saved: {message.id} from customer {customer_id}")
            
            return {
                "success": True,
                "message_id": message.id,
                "saved_at": datetime.utcnow()
            }
        except Exception as e:
            logger.error(f"Error saving customer interaction: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}
    
    async def update_lead_in_crm(
        self,
        db: Session,
        lead_id: str,
        **update_data
    ) -> Dict:
        """
        Update lead information in CRM
        
        Args:
            db: Database session
            lead_id: Lead ID
            **update_data: Fields to update
            
        Returns:
            Update result
        """
        try:
            lead = db.query(Lead).filter(Lead.id == lead_id).first()
            if not lead:
                return {"success": False, "error": "Lead not found"}
            
            # Update allowed fields
            allowed_fields = [
                "status", "quality_score", "requirements", "timeline",
                "budget", "priority", "notes", "assigned_to"
            ]
            
            for field, value in update_data.items():
                if field in allowed_fields and value is not None:
                    setattr(lead, field, value)
            
            lead.updated_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"Lead {lead_id} updated in CRM")
            
            return {"success": True, "lead_id": lead_id}
        except Exception as e:
            logger.error(f"Error updating lead in CRM: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}
    
    async def get_customer_history(
        self,
        db: Session,
        customer_id: str,
        limit: int = 50
    ) -> Dict:
        """
        Get customer interaction history
        
        Args:
            db: Database session
            customer_id: Customer ID
            limit: Number of messages to retrieve
            
        Returns:
            Interaction history
        """
        try:
            messages = db.query(Message)\
                .filter(Message.customer_id == customer_id)\
                .order_by(Message.created_at.desc())\
                .limit(limit)\
                .all()
            
            history = [
                {
                    "id": msg.id,
                    "direction": msg.direction,
                    "channel": msg.channel,
                    "content": msg.content,
                    "created_at": msg.created_at
                }
                for msg in messages
            ]
            
            return {
                "success": True,
                "customer_id": customer_id,
                "message_count": len(history),
                "history": history
            }
        except Exception as e:
            logger.error(f"Error retrieving customer history: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def sync_with_salesforce(
        self,
        lead_data: Dict
    ) -> Dict:
        """
        Sync lead data with Salesforce CRM
        
        Args:
            lead_data: Lead information to sync
            
        Returns:
            Sync result
        """
        # TODO: Implement Salesforce integration
        # This would use salesforce-python library or REST API
        logger.info(f"Syncing lead to Salesforce: {lead_data.get('id')}")
        
        return {
            "success": True,
            "message": "Salesforce sync queued"
        }
    
    async def tag_lead(
        self,
        db: Session,
        lead_id: str,
        tags: list
    ) -> Dict:
        """
        Add tags to lead for organization
        
        Args:
            db: Database session
            lead_id: Lead ID
            tags: List of tags to add
            
        Returns:
            Tagging result
        """
        try:
            lead = db.query(Lead).filter(Lead.id == lead_id).first()
            if not lead:
                return {"success": False, "error": "Lead not found"}
            
            # Store tags in notes or create a separate tags field
            existing_notes = lead.notes or ""
            tag_string = f"Tags: {', '.join(tags)}"
            
            if existing_notes:
                lead.notes = f"{existing_notes}\n{tag_string}"
            else:
                lead.notes = tag_string
            
            db.commit()
            
            return {"success": True, "lead_id": lead_id, "tags": tags}
        except Exception as e:
            logger.error(f"Error tagging lead: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}


# Singleton instance
_crm_service = None

def get_crm_service() -> CRMService:
    """Get or create CRM service instance"""
    global _crm_service
    if _crm_service is None:
        _crm_service = CRMService()
    return _crm_service
