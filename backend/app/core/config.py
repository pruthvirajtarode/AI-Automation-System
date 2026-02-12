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
    
    # CRM Configuration
    SALESFORCE_CLIENT_ID: str = ""
    SALESFORCE_CLIENT_SECRET: str = ""
    SALESFORCE_INSTANCE_URL: str = ""
    
    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    # Calendar/Booking Configuration
    GOOGLE_CALENDAR_API_KEY: str = ""
    CALENDLY_API_TOKEN: str = ""
    
    # Notification Settings
    NOTIFICATION_EMAIL: str = ""
    SLACK_WEBHOOK_URL: str = ""
    
    # AI Configuration
    AI_SMART_MODEL: str = "gpt-4"
    AI_CHEAP_MODEL: str = "gpt-3.5-turbo"
    AI_MODEL: str = "gpt-4"  # Default/Legacy
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 2000
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Application Settings
    APP_NAME: str = "Digital Dada AI Operations Agent"
    APP_VERSION: str = "1.0.0"
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    
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
