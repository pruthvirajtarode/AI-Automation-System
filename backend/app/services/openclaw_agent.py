"""
Openclaw Agent Service - Advanced AI Lead Automation Agent
Handles intelligent lead scoring, routing, and automated follow-ups
with AWS S3 integration for agent persistence
"""

import logging
import json
import boto3
from typing import List, Dict, Optional, Any
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)


class OpenclawAgent:
    """Advanced agent for lead automation and management"""
    
    def __init__(self):
        """Initialize Openclaw agent with AWS S3 integration"""
        self.s3_client = None
        self.bucket_name = settings.AWS_S3_BUCKET
        self.agent_id = "openclaw_agent_001"
        self.version = "1.0.0"
        
        # Initialize S3 if AWS credentials are available
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            self._initialize_s3()
    
    def _initialize_s3(self):
        """Initialize AWS S3 client"""
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            logger.info(f"AWS S3 client initialized for bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {str(e)}")
            self.s3_client = None
    
    async def score_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score a lead based on multiple factors
        
        Args:
            lead_data: Dictionary containing lead information
            
        Returns:
            Dictionary with lead score and ranking
        """
        try:
            score = self._calculate_lead_score(lead_data)
            
            result = {
                "lead_id": lead_data.get("id"),
                "score": score,
                "rank": self._get_rank(score),
                "timestamp": datetime.utcnow().isoformat(),
                "agent_id": self.agent_id,
                "recommendation": self._get_recommendation(score)
            }
            
            # Save to S3 if available
            await self._save_to_s3(f"leads/{lead_data.get('id')}/score.json", result)
            
            return result
        except Exception as e:
            logger.error(f"Error scoring lead: {str(e)}")
            return {
                "error": str(e),
                "lead_id": lead_data.get("id"),
                "score": 0
            }
    
    def _calculate_lead_score(self, lead_data: Dict[str, Any]) -> float:
        """Calculate lead score based on multiple factors"""
        score = 0.0
        
        # Company size factor (0-20)
        company_size = lead_data.get("company_size", 0)
        if company_size > 100:
            score += 20
        elif company_size > 50:
            score += 15
        elif company_size > 10:
            score += 10
        
        # Engagement factor (0-30)
        engagement_rate = lead_data.get("engagement_rate", 0)
        score += min(engagement_rate * 30, 30)
        
        # Budget factor (0-25)
        budget = lead_data.get("budget", 0)
        if budget > 50000:
            score += 25
        elif budget > 10000:
            score += 20
        elif budget > 1000:
            score += 10
        
        # Industry fit factor (0-15)
        industry = lead_data.get("industry", "")
        target_industries = ["technology", "finance", "healthcare", "retail"]
        if industry.lower() in target_industries:
            score += 15
        
        # Contact quality factor (0-10)
        has_valid_email = lead_data.get("email", "") and "@" in lead_data.get("email", "")
        has_phone = lead_data.get("phone", "")
        if has_valid_email and has_phone:
            score += 10
        elif has_valid_email or has_phone:
            score += 5
        
        return min(score, 100.0)  # Cap at 100
    
    def _get_rank(self, score: float) -> str:
        """Get rank based on score"""
        if score >= 80:
            return "A"
        elif score >= 60:
            return "B"
        elif score >= 40:
            return "C"
        elif score >= 20:
            return "D"
        else:
            return "F"
    
    def _get_recommendation(self, score: float) -> str:
        """Get recommendation based on score"""
        if score >= 80:
            return "Immediate follow-up recommended"
        elif score >= 60:
            return "Schedule follow-up within 24 hours"
        elif score >= 40:
            return "Add to nurture campaign"
        elif score >= 20:
            return "Keep in database for future engagement"
        else:
            return "Consider removing from active pipeline"
    
    async def route_lead(self, lead_data: Dict[str, Any], team_members: List[Dict]) -> Dict[str, Any]:
        """
        Route lead to appropriate team member
        
        Args:
            lead_data: Lead information
            team_members: Available team members with their capacities
            
        Returns:
            Routing assignment result
        """
        try:
            # Score the lead first
            score_result = await self.score_lead(lead_data)
            
            # Find best team member
            best_member = self._find_best_team_member(team_members)
            
            result = {
                "lead_id": lead_data.get("id"),
                "assigned_to": best_member.get("name") if best_member else None,
                "assigned_to_id": best_member.get("id") if best_member else None,
                "lead_score": score_result.get("score"),
                "timestamp": datetime.utcnow().isoformat(),
                "agent_id": self.agent_id
            }
            
            # Save routing decision
            await self._save_to_s3(f"routing/{lead_data.get('id')}/assignment.json", result)
            
            return result
        except Exception as e:
            logger.error(f"Error routing lead: {str(e)}")
            return {"error": str(e), "lead_id": lead_data.get("id")}
    
    def _find_best_team_member(self, team_members: List[Dict]) -> Optional[Dict]:
        """Find team member with lowest workload"""
        if not team_members:
            return None
        
        return min(team_members, key=lambda x: x.get("current_leads", 0))
    
    async def generate_followup(self, lead_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate intelligent follow-up message
        
        Args:
            lead_data: Lead information
            context: Additional context for personalization
            
        Returns:
            Generated follow-up message
        """
        try:
            message = self._compose_followup_message(lead_data, context)
            
            result = {
                "lead_id": lead_data.get("id"),
                "message": message,
                "generated_at": datetime.utcnow().isoformat(),
                "agent_id": self.agent_id,
                "personalized": True
            }
            
            # Save follow-up
            await self._save_to_s3(f"followups/{lead_data.get('id')}/message.json", result)
            
            return result
        except Exception as e:
            logger.error(f"Error generating follow-up: {str(e)}")
            return {"error": str(e), "lead_id": lead_data.get("id")}
    
    def _compose_followup_message(self, lead_data: Dict[str, Any], context: Optional[Dict] = None) -> str:
        """Compose personalized follow-up message"""
        name = lead_data.get("name", "there")
        company = lead_data.get("company", "")
        
        message = f"Hi {name},\n\n"
        message += "Thank you for your interest in our services. "
        
        if company:
            message += f"I noticed that {company} might benefit from our AI-powered lead automation solution. "
        
        message += "I'd love to schedule a brief call to discuss how we can help you.\n\n"
        message += "Best regards,\nYour AI Agent"
        
        return message
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status and statistics"""
        try:
            status = {
                "agent_id": self.agent_id,
                "version": self.version,
                "status": "active",
                "s3_enabled": self.s3_client is not None,
                "timestamp": datetime.utcnow().isoformat(),
                "capabilities": [
                    "lead_scoring",
                    "lead_routing",
                    "followup_generation",
                    "persistence_s3"
                ]
            }
            return status
        except Exception as e:
            logger.error(f"Error getting agent status: {str(e)}")
            return {"error": str(e), "agent_id": self.agent_id}
    
    async def _save_to_s3(self, key: str, data: Dict[str, Any]) -> bool:
        """Save agent data to AWS S3"""
        if not self.s3_client or not self.bucket_name:
            logger.warning("S3 client not available, skipping save")
            return False
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=json.dumps(data, indent=2),
                ContentType='application/json'
            )
            logger.info(f"Saved data to S3: {key}")
            return True
        except Exception as e:
            logger.error(f"Error saving to S3: {str(e)}")
            return False
    
    async def load_from_s3(self, key: str) -> Optional[Dict[str, Any]]:
        """Load agent data from AWS S3"""
        if not self.s3_client or not self.bucket_name:
            logger.warning("S3 client not available, skipping load")
            return None
        
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            data = json.loads(response['Body'].read().decode('utf-8'))
            logger.info(f"Loaded data from S3: {key}")
            return data
        except Exception as e:
            logger.error(f"Error loading from S3: {str(e)}")
            return None


# Initialize global agent instance
openclaw_agent = OpenclawAgent()
