"""
Lead Qualification Service
Intelligent lead analysis and scoring
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Lead, Customer

logger = logging.getLogger(__name__)

class LeadQualificationService:
    """Service for lead analysis and qualification"""
    
    def __init__(self):
        self.weights = {
            "budget": 0.25,
            "timeline": 0.25,
            "fit": 0.25,
            "intent": 0.25
        }
    
    async def qualify_lead(
        self,
        db: Session,
        customer_id: str,
        ai_qualification: Dict
    ) -> Dict:
        """
        Qualify a lead using AI assessment and business rules
        
        Args:
            db: Database session
            customer_id: Customer ID to qualify
            ai_qualification: AI qualification results
            
        Returns:
            Qualification result with score and priority
        """
        try:
            # Get customer and existing lead
            customer = db.query(Customer).filter(Customer.id == customer_id).first()
            if not customer:
                logger.error(f"Customer {customer_id} not found")
                return {"success": False, "error": "Customer not found"}
            
            # Calculate quality score based on multiple factors
            quality_score = self._calculate_quality_score(
                ai_qualification,
                customer
            )
            
            # Determine priority
            priority = self._determine_priority(quality_score)
            
            # Get recommendations
            recommendations = self._get_recommendations(quality_score, ai_qualification)
            
            # Update or create lead
            lead = db.query(Lead).filter(Lead.customer_id == customer_id).first()
            if lead:
                lead.quality_score = quality_score
                lead.priority = priority
                lead.updated_at = datetime.utcnow()
            else:
                lead = Lead(
                    customer_id=customer_id,
                    quality_score=quality_score,
                    priority=priority
                )
                db.add(lead)
            
            db.commit()
            
            return {
                "success": True,
                "lead_id": lead.id,
                "quality_score": quality_score,
                "priority": priority,
                "recommendations": recommendations
            }
        except Exception as e:
            logger.error(f"Error qualifying lead: {str(e)}")
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    def _calculate_quality_score(self, ai_qualification: Dict, customer: Customer) -> float:
        """Calculate lead quality score"""
        score = 0.0
        
        # AI quality score (base)
        ai_score = ai_qualification.get("quality_score", 50) / 100
        score += ai_score * self.weights["fit"]
        
        # Timeline assessment
        timeline = ai_qualification.get("timeline", "").lower()
        timeline_score = self._assess_timeline(timeline)
        score += timeline_score * self.weights["timeline"]
        
        # Budget assessment
        budget = ai_qualification.get("budget", "").lower()
        budget_score = self._assess_budget(budget)
        score += budget_score * self.weights["budget"]
        
        # Intent from conversation
        intent_score = ai_qualification.get("intent_score", 0.5)
        score += intent_score * self.weights["intent"]
        
        # Normalize to 0-100
        return min(100, max(0, score * 100))
    
    def _assess_timeline(self, timeline: str) -> float:
        """Assess timeline signal (0-1)"""
        if not timeline:
            return 0.5
        
        if any(word in timeline for word in ["urgent", "asap", "immediately", "week"]):
            return 1.0
        elif any(word in timeline for word in ["month", "soon"]):
            return 0.8
        elif any(word in timeline for word in ["quarter"]):
            return 0.6
        elif any(word in timeline for word in ["year", "later"]):
            return 0.3
        else:
            return 0.5
    
    def _assess_budget(self, budget: str) -> float:
        """Assess budget signal (0-1)"""
        if not budget:
            return 0.5
        
        if any(word in budget for word in ["large", "significant", "substantial", "unlimited"]):
            return 1.0
        elif any(word in budget for word in ["good", "decent", "reasonable"]):
            return 0.8
        elif any(word in budget for word in ["limited", "tight", "small"]):
            return 0.3
        else:
            return 0.5
    
    def _determine_priority(self, quality_score: float) -> str:
        """Determine lead priority based on score"""
        if quality_score >= 75:
            return "high"
        elif quality_score >= 50:
            return "medium"
        else:
            return "low"
    
    def _get_recommendations(self, quality_score: float, ai_qualification: Dict) -> List[str]:
        """Get action recommendations based on score"""
        recommendations = []
        
        if quality_score >= 75:
            recommendations.append("Schedule consultation call immediately")
            recommendations.append("Prepare custom proposal")
            recommendations.append("Assign to top sales representative")
        elif quality_score >= 50:
            recommendations.append("Send product information")
            recommendations.append("Schedule follow-up call")
            recommendations.append("Add to nurture sequence")
        else:
            recommendations.append("Send educational content")
            recommendations.append("Add to long-term nurture campaign")
        
        # Add AI recommendations if available
        if ai_qualification.get("recommended_next_steps"):
            recommendations.extend(ai_qualification["recommended_next_steps"][:2])
        
        return recommendations
    
    async def update_lead_qualification(self, db: Session, lead_id: str, **kwargs) -> Dict:
        """Update lead qualification data"""
        try:
            lead = db.query(Lead).filter(Lead.id == lead_id).first()
            if not lead:
                return {"success": False, "error": "Lead not found"}
            
            for key, value in kwargs.items():
                if hasattr(lead, key):
                    setattr(lead, key, value)
            
            lead.updated_at = datetime.utcnow()
            db.commit()
            
            return {"success": True, "lead": lead}
        except Exception as e:
            logger.error(f"Error updating lead qualification: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}


# Singleton instance
_qualification_service = None

def get_qualification_service() -> LeadQualificationService:
    """Get or create lead qualification service instance"""
    global _qualification_service
    if _qualification_service is None:
        _qualification_service = LeadQualificationService()
    return _qualification_service
