"""
CRM API Routes
Customer and CRM data management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import CustomerCreate, CustomerUpdate, CustomerResponse
from app.models import Customer, Message
from app.services.crm_service import get_crm_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/customers", response_model=CustomerResponse)
async def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    """Create new customer"""
    try:
        # Check if customer already exists
        existing = db.query(Customer).filter(
            (Customer.email == customer.email) | 
            (Customer.phone == customer.phone)
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Customer already exists")
        
        db_customer = Customer(**customer.dict())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        
        return db_customer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating customer: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customers", response_model=List[CustomerResponse])
async def list_customers(
    company: str = Query(None),
    business_type: str = Query(None),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    """List customers with optional filtering"""
    try:
        query = db.query(Customer)
        
        if company:
            query = query.filter(Customer.company.ilike(f"%{company}%"))
        if business_type:
            query = query.filter(Customer.business_type == business_type)
        
        customers = query.order_by(Customer.created_at.desc()).limit(limit).all()
        
        return customers
    except Exception as e:
        logger.error(f"Error listing customers: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    """Get specific customer details"""
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        return customer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting customer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/customers/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db)
):
    """Update customer information"""
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        update_data = customer_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)
        
        db.commit()
        db.refresh(customer)
        
        return customer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating customer: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customers/{customer_id}/history")
async def get_customer_history(
    customer_id: str,
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    """Get customer interaction history"""
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        crm_service = get_crm_service()
        
        history = await crm_service.get_customer_history(db, customer_id, limit)
        
        return history
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting customer history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/leads/{lead_id}/update")
async def update_lead_in_crm(
    lead_id: str,
    status: str = None,
    quality_score: float = None,
    notes: str = None,
    db: Session = Depends(get_db)
):
    """Update lead in CRM"""
    try:
        crm_service = get_crm_service()
        
        update_data = {}
        if status:
            update_data["status"] = status
        if quality_score is not None:
            update_data["quality_score"] = quality_score
        if notes:
            update_data["notes"] = notes
        
        result = await crm_service.update_lead_in_crm(db, lead_id, **update_data)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating lead in CRM: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync/salesforce")
async def sync_to_salesforce(
    lead_id: str,
    db: Session = Depends(get_db)
):
    """Sync lead to Salesforce CRM"""
    try:
        from app.models import Lead
        
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        crm_service = get_crm_service()
        
        result = await crm_service.sync_with_salesforce({
            "id": lead.id,
            "name": lead.customer.name,
            "email": lead.customer.email,
            "company": lead.customer.company,
            "status": lead.status,
            "quality_score": lead.quality_score
        })
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error syncing to Salesforce: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
