"""
n8n Integration Routes
General purpose webhook handler for n8n automations
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.core.database import get_db
from app.services.crm_service import get_crm_service
from app.services.ai_service import get_ai_service
from app.models import Customer, Lead, Message
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/process")
async def process_n8n_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle generalized intake from n8n.
    Standardized payload: { "trigger": "form", "data": {...}, "customer": {...} }
    """
    try:
        data = await request.json()
        logger.info(f"Received n8n webhook: {data.get('trigger', 'unknown')}")
        
        trigger_type = data.get("trigger", "general")
        payload = data.get("data", {})
        customer_info = data.get("customer", {})
        
        # 1. Handle Lead Ingestion
        if trigger_type == "lead" or trigger_type == "form":
            email = customer_info.get("email")
            if not email:
                return {"success": False, "error": "Email required for lead ingestion"}
            
            customer = db.query(Customer).filter(Customer.email == email).first()
            if not customer:
                customer = Customer(
                    email=email,
                    name=customer_info.get("name", "New Lead"),
                    phone=customer_info.get("phone", "Pending"),
                    company=customer_info.get("company", "")
                )
                db.add(customer)
                db.flush()
            
            # Create Lead record
            lead = Lead(
                customer_id=customer.id,
                status="new",
                source=data.get("source", "n8n_webhook")
            )
            db.add(lead)
            db.commit()
            
            # 2. Trigger AI Analysis (Optional)
            ai_service = get_ai_service()
            analysis = await ai_service.qualify_lead(lead.id, str(payload))
            
            return {
                "success": True, 
                "lead_id": lead.id, 
                "customer_id": customer.id,
                "ai_analysis": analysis
            }
            
        return {"success": True, "message": f"Trigger {trigger_type} acknowledged"}
        
    except Exception as e:
        logger.error(f"Error processing n8n webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
