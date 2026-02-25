"""
Application Configuration
Handles all environment variables and settings
"""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application Settings"""
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/ai_automation"
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "ai_automation"
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"
    
    # API Keys
    OPENAI_API_KEY: str = ""
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    SENDGRID_API_KEY: str = ""
    STRIPE_API_KEY: str = ""
    
    # GoHighLevel CRM Configuration
    GOHIGHLEVEL_API_KEY: str = ""
    GOHIGHLEVEL_LOCATION_ID: str = ""
    GOHIGHLEVEL_BASE_URL: str = "https://rest.gohighlevel.com/v1"
    GOHIGHLEVEL_CALENDAR_ID: str = ""
    GOHIGHLEVEL_PIPELINE_ID: str = ""
    GOHIGHLEVEL_STAGE_ID_NEW: str = ""
    GOHIGHLEVEL_STAGE_ID_BOOKED: str = ""
    
    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    # Zoho Mail Configuration
    ZOHO_MAIL_API_KEY: str = ""
    
    # Airtable Configuration
    AIRTABLE_TOKEN: str = ""
    
    # Calendar/Booking Configuration
    GOOGLE_CALENDAR_API_KEY: str = ""
    CALENDLY_API_TOKEN: str = ""
    
    # Notification Settings
    NOTIFICATION_EMAIL: str = ""
    SLACK_WEBHOOK_URL: str = ""
    
    # AI Configuration
    AI_SMART_MODEL: str = "gpt-4"
    AI_CHEAP_MODEL: str = "gpt-3.5-turbo"
    AI_MODEL: str = "gpt-4"
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 2000
    
    # Business Identity
    BUSINESS_NAME: str = "Digital Dada AI"
    BUSINESS_TAGLINE: str = "Your AI Operations Agent"
    BUSINESS_SERVICES: str = ""
    BUSINESS_HOURS: str = "Monday-Friday 9 AM-6 PM EST"
    BOOKING_URL: str = ""
    AI_AGENT_NAME: str = "Digital Dada AI Operations Agent"
    AI_TONE: str = "professional"
    
    # Trello Integration
    TRELLO_API_KEY: str = ""
    TRELLO_API_TOKEN: str = ""
    TRELLO_BOARD_ID: str = ""
    
    # n8n Workflow Automation
    N8N_BASE_URL: str = ""
    N8N_WEBHOOK_SECRET: str = ""
    N8N_INTAKE_WEBHOOK_URL: str = ""
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080", "*"]
    
    # Application Settings
    APP_NAME: str = "Digital Dada AI Operations Agent"
    APP_VERSION: str = "2.0.0"
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    
    # Admin Auth
    ADMIN_EMAIL: str = "admin@techsales.com"
    ADMIN_PASSWORD: str = "Admin@12345"

    
    # AWS Configuration
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str = "ai-automation-agent-data"
    
    # Deployment Environment
    DEPLOYMENT_ENV: str = "local"  # local, aws, docker
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

# Create global settings instance
settings = Settings()
