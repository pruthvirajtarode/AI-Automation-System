"""
Lead API Routes
Lead management and qualification endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import LeadCreate, LeadUpdate, LeadResponse, LeadQualificationRequest, LeadQualificationResponse
from app.models import Lead, Customer
from app.services.lead_service import get_qualification_service
from app.services.ai_service import get_ai_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=LeadResponse)
async def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db)
):
    """Create new lead - optionally auto-creates customer from inline fields"""
    try:
        customer_id = lead.customer_id

        # If no customer_id but name/email provided, find or create customer
        if not customer_id and (lead.name or lead.email):
            existing = None
            if lead.email:
                existing = db.query(Customer).filter(Customer.email == lead.email).first()
            if not existing and lead.phone:
                existing = db.query(Customer).filter(Customer.phone == lead.phone).first()

            if existing:
                customer_id = existing.id
            else:
                new_customer = Customer(
                    name=lead.name or "Unknown",
                    email=lead.email or "",
                    phone=lead.phone or "",
                    company=lead.company or "",
                )
                db.add(new_customer)
                db.flush()
                customer_id = new_customer.id

        if not customer_id:
            raise HTTPException(status_code=400, detail="Either customer_id or customer fields (name, email) required")

        lead_data = {
            "customer_id": customer_id,
            "status": lead.status or "new",
            "quality_score": lead.quality_score or 0.0,
            "requirements": lead.requirements,
            "timeline": lead.timeline,
            "budget": lead.budget,
            "priority": lead.priority,
            "assigned_to": lead.assigned_to,
        }
        db_lead = Lead(**lead_data)
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)

        # Attach customer info for response
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        return _lead_with_customer(db_lead, customer)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating lead: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def _lead_with_customer(lead, customer=None):
    """Build LeadResponse dict with customer info attached"""
    return {
        "id": lead.id,
        "customer_id": lead.customer_id,
        "status": lead.status.value if hasattr(lead.status, 'value') else lead.status,
        "quality_score": lead.quality_score,
        "requirements": lead.requirements,
        "timeline": lead.timeline,
        "budget": lead.budget,
        "priority": lead.priority,
        "assigned_to": lead.assigned_to,
        "name": customer.name if customer else None,
        "company": customer.company if customer else None,
        "email": customer.email if customer else None,
        "phone": customer.phone if customer else None,
        "created_at": lead.created_at,
        "updated_at": lead.updated_at,
    }


@router.get("/", response_model=List[LeadResponse])
async def list_leads(
    status: str = Query(None),
    priority: str = Query(None),
    assigned_to: str = Query(None),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    """List leads with customer info"""
    try:
        query = db.query(Lead)
        
        if status:
            query = query.filter(Lead.status == status)
        if priority:
            query = query.filter(Lead.priority == priority)
        if assigned_to:
            query = query.filter(Lead.assigned_to == assigned_to)
        
        leads = query.order_by(Lead.created_at.desc()).limit(limit).all()

        result = []
        for lead in leads:
            customer = db.query(Customer).filter(Customer.id == lead.customer_id).first()
            result.append(_lead_with_customer(lead, customer))
        return result
    except Exception as e:
        logger.error(f"Error listing leads: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: str,
    db: Session = Depends(get_db)
):
    """Get specific lead details"""
    try:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        return lead
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting lead: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: str,
    lead_update: LeadUpdate,
    db: Session = Depends(get_db)
):
    """Update lead information"""
    try:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        update_data = lead_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(lead, field, value)
        
        db.commit()
        db.refresh(lead)
        
        return lead
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating lead: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{lead_id}")
async def delete_lead(
    lead_id: str,
    db: Session = Depends(get_db)
):
    """Delete lead"""
    try:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        db.delete(lead)
        db.commit()
        
        return {"status": "deleted", "lead_id": lead_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting lead: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{lead_id}/qualify", response_model=LeadQualificationResponse)
async def qualify_lead(
    lead_id: str,
    request: LeadQualificationRequest,
    db: Session = Depends(get_db)
):
    """
    Qualify lead using AI analysis
    """
    try:
        # Get lead
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        # Use AI to qualify
        ai_service = get_ai_service()
        ai_result = await ai_service.qualify_lead(
            {
                "name": lead.customer.name,
                "company": lead.customer.company,
                "business_type": lead.customer.business_type
            },
            [{"role": "user", "content": request.message_content}]
        )
        
        if not ai_result.get("success"):
            raise HTTPException(status_code=400, detail="Failed to qualify lead")
        
        # Update lead with qualification results
        qual_service = get_qualification_service()
        qual_result = await qual_service.qualify_lead(
            db, lead.customer_id, ai_result["qualification"]
        )
        
        if not qual_result.get("success"):
            raise HTTPException(status_code=400, detail="Failed to update lead")
        
        return LeadQualificationResponse(
            quality_score=qual_result["quality_score"],
            priority=qual_result["priority"],
            recommendations=qual_result["recommendations"],
            next_actions=qual_result.get("recommendations", [])
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error qualifying lead: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{lead_id}/assign")
async def assign_lead(
    lead_id: str,
    assigned_to: str,
    db: Session = Depends(get_db)
):
    """Assign lead to team member"""
    try:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        lead.assigned_to = assigned_to
        db.commit()
        
        return {"status": "assigned", "lead_id": lead_id, "assigned_to": assigned_to}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning lead: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
