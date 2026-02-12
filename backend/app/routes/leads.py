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
    """Create new lead"""
    try:
        # Verify customer exists
        customer = db.query(Customer).filter(Customer.id == lead.customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        db_lead = Lead(**lead.dict())
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
        
        return db_lead
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating lead: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[LeadResponse])
async def list_leads(
    status: str = Query(None),
    priority: str = Query(None),
    assigned_to: str = Query(None),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    """List leads with optional filtering"""
    try:
        query = db.query(Lead)
        
        if status:
            query = query.filter(Lead.status == status)
        if priority:
            query = query.filter(Lead.priority == priority)
        if assigned_to:
            query = query.filter(Lead.assigned_to == assigned_to)
        
        leads = query.order_by(Lead.created_at.desc()).limit(limit).all()
        
        return leads
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
