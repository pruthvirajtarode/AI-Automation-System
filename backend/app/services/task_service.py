"""
Task Routing Service
Routes tasks to appropriate teams based on content
"""

import logging
from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Task, Lead

logger = logging.getLogger(__name__)

class TaskRoutingService:
    """Service for automatic task routing and team assignment"""
    
    def __init__(self):
        self.routing_rules = {
            "sales": {
                "keywords": ["interested", "buy", "purchase", "pricing", "demo", "trial"],
                "team": "sales",
                "priority": "high"
            },
            "support": {
                "keywords": ["issue", "problem", "error", "bug", "not working", "help"],
                "team": "support",
                "priority": "medium"
            },
            "technical": {
                "keywords": ["integration", "api", "technical", "implementation", "setup"],
                "team": "technical",
                "priority": "high"
            },
            "general": {
                "keywords": [],
                "team": "sales",
                "priority": "medium"
            }
        }
    
    async def route_task(
        self,
        db: Session,
        lead_id: str,
        message_content: str,
        **kwargs
    ) -> Dict:
        """
        Route task to appropriate team based on content
        
        Args:
            db: Database session
            lead_id: Lead ID
            message_content: Message or task content
            **kwargs: Additional task data
            
        Returns:
            Task routing result
        """
        try:
            # Determine task type and team
            task_type, assigned_team, priority = self._analyze_content(message_content)
            
            # Create task
            task = Task(
                lead_id=lead_id,
                title=kwargs.get("title", f"{task_type.capitalize()} Task"),
                description=message_content,
                task_type=task_type,
                assigned_to=assigned_team,
                priority=priority,
                status="open",
                due_date=self._calculate_due_date(priority)
            )
            
            db.add(task)
            db.commit()
            
            # Send notification to team
            await self._notify_team(assigned_team, task)
            
            logger.info(f"Task routed to {assigned_team}: {task.id}")
            
            return {
                "success": True,
                "task_id": task.id,
                "routed_to": assigned_team,
                "task_type": task_type,
                "priority": priority
            }
        except Exception as e:
            logger.error(f"Error routing task: {str(e)}")
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    def _analyze_content(self, content: str) -> tuple:
        """
        Analyze message content to determine routing
        
        Args:
            content: Message content
            
        Returns:
            Tuple of (task_type, assigned_team, priority)
        """
        content_lower = content.lower()
        
        # Check against routing rules
        for rule_type, rule in self.routing_rules.items():
            if rule["keywords"]:
                if any(keyword in content_lower for keyword in rule["keywords"]):
                    return (rule["team"], rule["team"], rule["priority"])
        
        # Default routing
        return ("general", self.routing_rules["general"]["team"], self.routing_rules["general"]["priority"])
    
    def _calculate_due_date(self, priority: str) -> datetime:
        """
        Calculate due date based on priority
        
        Args:
            priority: Task priority (high, medium, low)
            
        Returns:
            Due date datetime
        """
        now = datetime.utcnow()
        
        if priority == "high":
            return now + timedelta(hours=4)
        elif priority == "medium":
            return now + timedelta(days=1)
        else:
            return now + timedelta(days=3)
    
    async def _notify_team(self, team: str, task: Task) -> Dict:
        """
        Send notification to assigned team
        
        Args:
            team: Team name
            task: Task object
            
        Returns:
            Notification result
        """
        # TODO: Integrate with notification service (Slack, email, etc.)
        notification_message = f"New {task.task_type} task assigned: {task.title}"
        
        logger.info(f"Notifying {team}: {notification_message}")
        
        return {"success": True, "team": team}
    
    async def update_task_status(
        self,
        db: Session,
        task_id: str,
        status: str
    ) -> Dict:
        """
        Update task status
        
        Args:
            db: Database session
            task_id: Task ID
            status: New status
            
        Returns:
            Update result
        """
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                return {"success": False, "error": "Task not found"}
            
            task.status = status
            task.updated_at = datetime.utcnow()
            db.commit()
            
            return {"success": True, "task_id": task_id, "status": status}
        except Exception as e:
            logger.error(f"Error updating task status: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}
    
    async def assign_task(
        self,
        db: Session,
        task_id: str,
        assigned_to: str
    ) -> Dict:
        """
        Assign task to specific person
        
        Args:
            db: Database session
            task_id: Task ID
            assigned_to: Person to assign to
            
        Returns:
            Assignment result
        """
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                return {"success": False, "error": "Task not found"}
            
            task.assigned_to = assigned_to
            task.updated_at = datetime.utcnow()
            db.commit()
            
            return {"success": True, "task_id": task_id, "assigned_to": assigned_to}
        except Exception as e:
            logger.error(f"Error assigning task: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}


# Singleton instance
_task_routing_service = None

def get_task_routing_service() -> TaskRoutingService:
    """Get or create task routing service instance"""
    global _task_routing_service
    if _task_routing_service is None:
        _task_routing_service = TaskRoutingService()
    return _task_routing_service
