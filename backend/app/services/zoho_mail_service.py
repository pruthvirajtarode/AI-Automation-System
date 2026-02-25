"""
Zoho Mail Integration Service
Sends transactional and notification emails via Zoho Mail API.
"""

import logging
from typing import Dict, Optional

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

ZOHO_MAIL_API = "https://mail.zoho.com/api"


class ZohoMailService:
    """Handles email operations through Zoho Mail API."""

    def __init__(self):
        self.api_key = settings.ZOHO_MAIL_API_KEY
        self._configured = bool(self.api_key)

        if not self._configured:
            logger.warning("Zoho Mail service not configured – API key missing.")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Zoho-oauthtoken {self.api_key}",
            "Content-Type": "application/json",
        }

    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        from_address: str = "",
        is_html: bool = False,
    ) -> Dict:
        """
        Send an email through Zoho Mail.

        Args:
            to: Recipient email address.
            subject: Email subject line.
            body: Email body (plain text or HTML).
            from_address: Sender address (uses account default if empty).
            is_html: Whether the body is HTML.

        Returns:
            Result dict with success status.
        """
        if not self._configured:
            logger.debug("Zoho Mail send skipped – not configured.")
            return {"success": False, "error": "Zoho Mail not configured"}

        payload = {
            "fromAddress": from_address,
            "toAddress": to,
            "subject": subject,
            "content": body,
            "mailFormat": "html" if is_html else "plaintext",
        }

        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post(
                    f"{ZOHO_MAIL_API}/accounts/me/messages",
                    headers=self._headers(),
                    json=payload,
                )
                resp.raise_for_status()
                data = resp.json()
                logger.info(f"Zoho Mail sent to {to}: {subject}")
                return {"success": True, "data": data}
        except Exception as exc:
            logger.error(f"Error sending Zoho Mail: {exc}")
            return {"success": False, "error": str(exc)}

    async def send_lead_notification(
        self,
        lead_name: str,
        lead_email: str,
        lead_company: str,
        notification_to: str,
    ) -> Dict:
        """Send a 'New Lead' notification email."""
        subject = f"🔔 New Lead: {lead_name} from {lead_company}"
        body = f"""
        <h2>New Lead Received</h2>
        <table style="border-collapse:collapse;">
            <tr><td><strong>Name:</strong></td><td>{lead_name}</td></tr>
            <tr><td><strong>Email:</strong></td><td>{lead_email}</td></tr>
            <tr><td><strong>Company:</strong></td><td>{lead_company}</td></tr>
        </table>
        <p>View and manage in the <a href="#">Digital Dada Dashboard</a>.</p>
        """
        return await self.send_email(to=notification_to, subject=subject, body=body, is_html=True)

    async def send_booking_confirmation(
        self,
        to: str,
        customer_name: str,
        meeting_time: str,
        meeting_link: str,
    ) -> Dict:
        """Send a booking confirmation email to the customer."""
        subject = f"✅ Your appointment is confirmed – {settings.BUSINESS_NAME}"
        body = f"""
        <h2>Appointment Confirmed</h2>
        <p>Hi {customer_name},</p>
        <p>Your consultation with <strong>{settings.BUSINESS_NAME}</strong> is confirmed.</p>
        <table style="border-collapse:collapse;">
            <tr><td><strong>Time:</strong></td><td>{meeting_time}</td></tr>
            <tr><td><strong>Meeting Link:</strong></td><td><a href="{meeting_link}">{meeting_link}</a></td></tr>
        </table>
        <p>If you need to reschedule, please reply to this email.</p>
        <p>Best regards,<br/>{settings.BUSINESS_NAME}</p>
        """
        return await self.send_email(to=to, subject=subject, body=body, is_html=True)


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------

_zoho_service: Optional[ZohoMailService] = None


def get_zoho_mail_service() -> ZohoMailService:
    global _zoho_service
    if _zoho_service is None:
        _zoho_service = ZohoMailService()
    return _zoho_service
