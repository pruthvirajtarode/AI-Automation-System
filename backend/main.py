#!/usr/bin/env python3
"""
AI-Powered Messaging & Lead Automation System
Main application entry point
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import messages, leads, crm, bookings, tasks, follow_ups, openclaw, auth, n8n
from app.core.config import settings
from app.core.database import init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Lead Automation System",
    description="Automated customer communication and lead qualification",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])
app.include_router(leads.router, prefix="/api/leads", tags=["Leads"])
app.include_router(crm.router, prefix="/api/crm", tags=["CRM"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(follow_ups.router, prefix="/api/follow-ups", tags=["Follow-ups"])
app.include_router(openclaw.router, prefix="/api/agent", tags=["Openclaw Agent"])
app.include_router(n8n.router, prefix="/api/n8n", tags=["n8n Automation"])

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    init_db()
    logger.info("Application started successfully")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Lead Automation System",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "operational",
        "database": "connected",
        "ai_service": "ready"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
