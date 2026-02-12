"""
Task API Routes
Task management and routing endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.models import Task, Lead
from app.services.task_service import get_task_routing_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    """Create new task"""
    try:
        # Verify lead exists
        lead = db.query(Lead).filter(Lead.id == task.lead_id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        db_task = Task(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    status: str = Query(None),
    assigned_to: str = Query(None),
    task_type: str = Query(None),
    priority: str = Query(None),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    """List tasks with optional filtering"""
    try:
        query = db.query(Task)
        
        if status:
            query = query.filter(Task.status == status)
        if assigned_to:
            query = query.filter(Task.assigned_to == assigned_to)
        if task_type:
            query = query.filter(Task.task_type == task_type)
        if priority:
            query = query.filter(Task.priority == priority)
        
        tasks = query.order_by(Task.created_at.desc()).limit(limit).all()
        
        return tasks
    except Exception as e:
        logger.error(f"Error listing tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """Get specific task details"""
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update task information"""
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        db.commit()
        db.refresh(task)
        
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{lead_id}/route")
async def route_task(
    lead_id: str,
    message_content: str,
    title: str = None,
    db: Session = Depends(get_db)
):
    """
    Automatically route task to appropriate team
    """
    try:
        task_service = get_task_routing_service()
        
        result = await task_service.route_task(
            db,
            lead_id,
            message_content,
            title=title
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error routing task: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{task_id}/assign")
async def assign_task(
    task_id: str,
    assigned_to: str,
    db: Session = Depends(get_db)
):
    """Assign task to team member"""
    try:
        task_service = get_task_routing_service()
        
        result = await task_service.assign_task(db, task_id, assigned_to)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning task: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{task_id}/status/{status}")
async def update_task_status(
    task_id: str,
    status: str,
    db: Session = Depends(get_db)
):
    """Update task status"""
    try:
        task_service = get_task_routing_service()
        
        result = await task_service.update_task_status(db, task_id, status)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task status: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
