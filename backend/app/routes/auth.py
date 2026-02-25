"""
Authentication Routes
Simple token-based authentication for the admin dashboard
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.config import settings
import hashlib
import time
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user: dict


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Authenticate admin user"""
    if (
        request.email == settings.ADMIN_EMAIL
        and request.password == settings.ADMIN_PASSWORD
    ):
        # Generate a simple token
        raw = f"{request.email}:{settings.SECRET_KEY}:{int(time.time())}"
        token = hashlib.sha256(raw.encode()).hexdigest()

        logger.info(f"Successful login for {request.email}")
        return LoginResponse(
            token=token,
            user={
                "email": request.email,
                "name": "Admin",
                "role": "Administrator",
            },
        )

    logger.warning(f"Failed login attempt for {request.email}")
    raise HTTPException(status_code=401, detail="Invalid email or password")


@router.get("/me")
async def get_current_user():
    """Return current user info (for session validation)"""
    return {
        "email": settings.ADMIN_EMAIL,
        "name": "Admin",
        "role": "Administrator",
    }
