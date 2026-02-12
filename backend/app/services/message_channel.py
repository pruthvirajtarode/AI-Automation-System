"""
Message Channel Handlers
Handles multiple communication channels (SMS, Email, Chat, Forms)
"""

import logging
from typing import Dict, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class ChannelHandler(ABC):
    """Abstract base class for message channel handlers"""
    
    @abstractmethod
    async def send_message(self, recipient: str, content: str, **kwargs) -> Dict:
        """Send message through channel"""
        pass
    
    @abstractmethod
    async def receive_message(self, data: Dict) -> Dict:
        """Receive message from channel"""
        pass


class SMSHandler(ChannelHandler):
    """SMS message handler using Twilio"""
    
    def __init__(self):
        from app.core.config import settings
        try:
            from twilio.rest import Client
            self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            self.phone_number = settings.TWILIO_PHONE_NUMBER
        except Exception as e:
            logger.error(f"Error initializing SMS handler: {str(e)}")
    
    async def send_message(self, recipient: str, content: str, **kwargs) -> Dict:
        """Send SMS message"""
        try:
            message = self.client.messages.create(
                body=content,
                from_=self.phone_number,
                to=recipient
            )
            
            logger.info(f"SMS sent to {recipient}: {message.sid}")
            
            return {
                "success": True,
                "channel": "sms",
                "message_id": message.sid,
                "status": message.status
            }
        except Exception as e:
            logger.error(f"Error sending SMS: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def receive_message(self, data: Dict) -> Dict:
        """Process incoming SMS"""
        return {
            "success": True,
            "channel": "sms",
            "phone": data.get("From"),
            "content": data.get("Body"),
            "message_id": data.get("MessageSid")
        }


class EmailHandler(ChannelHandler):
    """Email message handler using SendGrid or SMTP"""
    
    def __init__(self):
        from app.core.config import settings
        self.api_key = settings.SENDGRID_API_KEY
        self.sender_email = settings.SMTP_USER
    
    async def send_message(self, recipient: str, content: str, **kwargs) -> Dict:
        """Send email message"""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            
            subject = kwargs.get("subject", "Message from AI Automation System")
            
            message = Mail(
                from_email=self.sender_email,
                to_emails=recipient,
                subject=subject,
                plain_text_content=content
            )
            
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
            logger.info(f"Email sent to {recipient}: {response.status_code}")
            
            return {
                "success": True,
                "channel": "email",
                "recipient": recipient,
                "status_code": response.status_code
            }
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def receive_message(self, data: Dict) -> Dict:
        """Process incoming email (webhook)"""
        return {
            "success": True,
            "channel": "email",
            "sender": data.get("from"),
            "subject": data.get("subject"),
            "content": data.get("text") or data.get("html"),
            "message_id": data.get("message_id")
        }


class ChatHandler(ChannelHandler):
    """Website chat handler"""
    
    async def send_message(self, recipient: str, content: str, **kwargs) -> Dict:
        """Send chat message"""
        try:
            # TODO: Implement actual chat backend integration
            # This could integrate with services like Intercom, Drift, etc.
            
            return {
                "success": True,
                "channel": "chat",
                "recipient": recipient,
                "message_id": kwargs.get("session_id")
            }
        except Exception as e:
            logger.error(f"Error sending chat message: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def receive_message(self, data: Dict) -> Dict:
        """Process incoming chat message"""
        return {
            "success": True,
            "channel": "chat",
            "session_id": data.get("session_id"),
            "user_id": data.get("user_id"),
            "content": data.get("message"),
            "timestamp": data.get("timestamp")
        }


class FormHandler(ChannelHandler):
    """Web form submission handler"""
    
    async def send_message(self, recipient: str, content: str, **kwargs) -> Dict:
        """Send form response (follow-up email)"""
        try:
            # Send confirmation/response email
            from app.services.message_channel import EmailHandler
            handler = EmailHandler()
            
            result = await handler.send_message(
                recipient=recipient,
                content=content,
                subject=kwargs.get("subject", "Thank you for your submission")
            )
            
            return result
        except Exception as e:
            logger.error(f"Error sending form response: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def receive_message(self, data: Dict) -> Dict:
        """Process form submission"""
        return {
            "success": True,
            "channel": "form",
            "email": data.get("email"),
            "name": data.get("name"),
            "company": data.get("company"),
            "message": data.get("message"),
            "form_id": data.get("form_id")
        }


class ChannelFactory:
    """Factory for creating channel handlers"""
    
    _handlers = {
        "sms": SMSHandler,
        "email": EmailHandler,
        "chat": ChatHandler,
        "form": FormHandler
    }
    
    @classmethod
    def get_handler(cls, channel: str) -> Optional[ChannelHandler]:
        """Get appropriate handler for channel"""
        handler_class = cls._handlers.get(channel.lower())
        if handler_class:
            return handler_class()
        
        logger.warning(f"Unknown channel: {channel}")
        return None
    
    @classmethod
    async def send_message(
        cls,
        channel: str,
        recipient: str,
        content: str,
        **kwargs
    ) -> Dict:
        """Send message through specified channel"""
        handler = cls.get_handler(channel)
        if not handler:
            return {"success": False, "error": f"Unknown channel: {channel}"}
        
        return await handler.send_message(recipient, content, **kwargs)


# Singleton instances
_sms_handler = None
_email_handler = None
_chat_handler = None
_form_handler = None

def get_sms_handler() -> SMSHandler:
    global _sms_handler
    if _sms_handler is None:
        _sms_handler = SMSHandler()
    return _sms_handler

def get_email_handler() -> EmailHandler:
    global _email_handler
    if _email_handler is None:
        _email_handler = EmailHandler()
    return _email_handler

def get_chat_handler() -> ChatHandler:
    global _chat_handler
    if _chat_handler is None:
        _chat_handler = ChatHandler()
    return _chat_handler

def get_form_handler() -> FormHandler:
    global _form_handler
    if _form_handler is None:
        _form_handler = FormHandler()
    return _form_handler
