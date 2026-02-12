"""
Openclaw Agent API Routes
Advanced lead automation agent endpoints
Handles lead scoring, routing, and intelligent follow-ups
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.services.openclaw_agent import openclaw_agent
from app.core.database import get_db
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# ============================================================================
# PYDANTIC MODELS FOR REQUEST/RESPONSE
# ============================================================================

class LeadScoreRequest(BaseModel):
    """Request model for lead scoring"""
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    company_size: Optional[int] = None
    industry: Optional[str] = None
    engagement_rate: Optional[float] = None
    budget: Optional[float] = None
    
    class Config:
        example = {
            "id": "lead_123",
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "company": "Tech Corp",
            "company_size": 150,
            "industry": "technology",
            "engagement_rate": 0.85,
            "budget": 50000
        }


class LeadScoreResponse(BaseModel):
    """Response model for lead scoring"""
    lead_id: str
    score: float
    rank: str
    recommendation: str
    timestamp: str
    agent_id: str
    
    class Config:
        example = {
            "lead_id": "lead_123",
            "score": 87.5,
            "rank": "A",
            "recommendation": "Immediate follow-up recommended",
            "timestamp": "2026-02-07T12:00:00",
            "agent_id": "openclaw_agent_001"
        }


class TeamMember(BaseModel):
    """Team member model"""
    id: str
    name: str
    email: str
    current_leads: int = 0


class LeadRoutingRequest(BaseModel):
    """Request model for lead routing"""
    lead: LeadScoreRequest
    team_members: List[TeamMember]


class LeadRoutingResponse(BaseModel):
    """Response model for lead routing"""
    lead_id: str
    assigned_to: Optional[str]
    assigned_to_id: Optional[str]
    lead_score: float
    timestamp: str
    agent_id: str


class FollowupRequest(BaseModel):
    """Request model for follow-up generation"""
    id: str
    name: str
    company: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class FollowupResponse(BaseModel):
    """Response model for follow-up generation"""
    lead_id: str
    message: str
    generated_at: str
    agent_id: str
    personalized: bool


class AgentStatusResponse(BaseModel):
    """Response model for agent status"""
    agent_id: str
    version: str
    status: str
    s3_enabled: bool
    timestamp: str
    capabilities: List[str]


# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.post("/score", response_model=LeadScoreResponse)
async def score_lead(request: LeadScoreRequest):
    """
    Score a lead using the Openclaw agent
    
    Calculates lead quality score based on:
    - Company size
    - Engagement rate
    - Budget
    - Industry fit
    - Contact quality
    
    Returns a score (0-100) and ranking (A-F)
    """
    try:
        logger.info(f"Scoring lead: {request.id}")
        
        result = await openclaw_agent.score_lead(request.dict())
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return LeadScoreResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in score_lead: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error scoring lead: {str(e)}")


@router.post("/route", response_model=LeadRoutingResponse)
async def route_lead(request: LeadRoutingRequest):
    """
    Route a lead to the best available team member
    
    Considers:
    - Lead quality score
    - Team member workload
    - Skills match
    
    Returns assigned team member information
    """
    try:
        logger.info(f"Routing lead: {request.lead.id}")
        
        result = await openclaw_agent.route_lead(
            request.lead.dict(),
            [member.dict() for member in request.team_members]
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return LeadRoutingResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in route_lead: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error routing lead: {str(e)}")


@router.post("/followup", response_model=FollowupResponse)
async def generate_followup(request: FollowupRequest):
    """
    Generate an intelligent, personalized follow-up message
    
    Uses the lead data and context to create a relevant follow-up
    that increases conversion probability
    """
    try:
        logger.info(f"Generating follow-up for lead: {request.id}")
        
        result = await openclaw_agent.generate_followup(
            request.dict(),
            request.context
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return FollowupResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in generate_followup: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating follow-up: {str(e)}")


@router.post("/batch-score")
async def batch_score_leads(leads: List[LeadScoreRequest]):
    """
    Score multiple leads in batch
    
    More efficient for processing large numbers of leads
    """
    try:
        logger.info(f"Batch scoring {len(leads)} leads")
        
        results = []
        for lead_data in leads:
            result = await openclaw_agent.score_lead(lead_data.dict())
            results.append(result)
        
        return {
            "total": len(leads),
            "processed": len(results),
            "scores": results
        }
    
    except Exception as e:
        logger.error(f"Error in batch_score_leads: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error batch scoring leads: {str(e)}")


@router.get("/status", response_model=AgentStatusResponse)
async def get_agent_status():
    """
    Get Openclaw agent status and capabilities
    
    Returns:
    - Agent version
    - Operational status
    - Enabled features
    - AWS S3 integration status
    """
    try:
        logger.info("Fetching agent status")
        
        status = await openclaw_agent.get_agent_status()
        
        if "error" in status:
            raise HTTPException(status_code=500, detail=status.get("error"))
        
        return AgentStatusResponse(**status)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_agent_status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting agent status: {str(e)}")


@router.get("/health")
async def agent_health_check():
    """
    Health check endpoint for the Openclaw agent
    
    Verifies agent is running and responsive
    """
    try:
        status = await openclaw_agent.get_agent_status()
        
        return {
            "status": "healthy",
            "agent_id": status.get("agent_id"),
            "operational": status.get("status") == "active"
        }
    
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@router.post("/s3/save")
async def save_data_to_s3(
    key: str,
    data: Dict[str, Any]
):
    """
    Save arbitrary data to AWS S3
    
    Useful for persisting agent decisions and analysis
    """
    try:
        logger.info(f"Saving data to S3: {key}")
        
        success = await openclaw_agent._save_to_s3(key, data)
        
        return {
            "success": success,
            "key": key,
            "message": "Data saved successfully" if success else "Failed to save data"
        }
    
    except Exception as e:
        logger.error(f"Error saving to S3: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving to S3: {str(e)}")


@router.get("/s3/load")
async def load_data_from_s3(key: str):
    """
    Load data from AWS S3
    
    Retrieves previously saved agent data
    """
    try:
        logger.info(f"Loading data from S3: {key}")
        
        data = await openclaw_agent.load_from_s3(key)
        
        if data is None:
            raise HTTPException(status_code=404, detail="Data not found in S3")
        
        return {
            "key": key,
            "data": data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error loading from S3: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error loading from S3: {str(e)}")
