"""
GoHighLevel (GHL) CRM Integration Service
Handles contacts, pipelines, opportunities, calendars, and SMS via the GHL REST API v1.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class GoHighLevelService:
    """Full GoHighLevel REST API integration."""

    def __init__(self):
        self.api_key = settings.GOHIGHLEVEL_API_KEY
        self.base_url = settings.GOHIGHLEVEL_BASE_URL.rstrip("/")
        self.location_id = settings.GOHIGHLEVEL_LOCATION_ID
        self.pipeline_id = settings.GOHIGHLEVEL_PIPELINE_ID
        self.stage_new = settings.GOHIGHLEVEL_STAGE_ID_NEW
        self.stage_booked = settings.GOHIGHLEVEL_STAGE_ID_BOOKED
        self.calendar_id = settings.GOHIGHLEVEL_CALENDAR_ID
        self._configured = bool(self.api_key)

        if not self._configured:
            logger.warning("GoHighLevel service not configured – API key missing.")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def _request(
        self, method: str, path: str, json: Optional[Dict] = None, params: Optional[Dict] = None
    ) -> Optional[Dict]:
        if not self._configured:
            logger.debug("GHL request skipped – service not configured.")
            return None

        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.request(
                method, url, headers=self._headers(), json=json, params=params
            )
            resp.raise_for_status()
            return resp.json()

    # ------------------------------------------------------------------
    # Contacts
    # ------------------------------------------------------------------

    async def create_contact(
        self,
        first_name: str,
        last_name: str = "",
        email: str = "",
        phone: str = "",
        company: str = "",
        tags: Optional[List[str]] = None,
    ) -> Optional[Dict]:
        """Create a new contact in GoHighLevel."""
        payload: Dict = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phone": phone,
            "companyName": company,
            "locationId": self.location_id,
        }
        if tags:
            payload["tags"] = tags

        try:
            result = await self._request("POST", "/contacts/", json=payload)
            if result:
                contact = result.get("contact", result)
                logger.info(f"GHL contact created: {contact.get('id')} – {first_name} {last_name}")
            return result
        except Exception as exc:
            logger.error(f"Error creating GHL contact: {exc}")
            return None

    async def get_contact(self, contact_id: str) -> Optional[Dict]:
        """Get contact by ID."""
        try:
            return await self._request("GET", f"/contacts/{contact_id}")
        except Exception as exc:
            logger.error(f"Error fetching GHL contact {contact_id}: {exc}")
            return None

    async def search_contacts(self, query: str) -> List[Dict]:
        """Search contacts by name/email/phone."""
        try:
            result = await self._request(
                "GET", "/contacts/", params={"query": query, "locationId": self.location_id}
            )
            return result.get("contacts", []) if result else []
        except Exception as exc:
            logger.error(f"Error searching GHL contacts: {exc}")
            return []

    async def update_contact(self, contact_id: str, **fields) -> Optional[Dict]:
        """Update contact fields."""
        try:
            return await self._request("PUT", f"/contacts/{contact_id}", json=fields)
        except Exception as exc:
            logger.error(f"Error updating GHL contact {contact_id}: {exc}")
            return None

    async def add_tags(self, contact_id: str, tags: List[str]) -> Optional[Dict]:
        """Add tags to a contact."""
        return await self.update_contact(contact_id, tags=tags)

    # ------------------------------------------------------------------
    # Pipeline / Opportunities
    # ------------------------------------------------------------------

    async def create_opportunity(
        self,
        contact_id: str,
        title: str,
        stage_id: Optional[str] = None,
        monetary_value: float = 0,
    ) -> Optional[Dict]:
        """Create a pipeline opportunity for a contact."""
        payload = {
            "pipelineId": self.pipeline_id,
            "locationId": self.location_id,
            "contactId": contact_id,
            "name": title,
            "pipelineStageId": stage_id or self.stage_new,
            "monetaryValue": monetary_value,
            "status": "open",
        }
        try:
            result = await self._request("POST", "/pipelines/opportunities", json=payload)
            if result:
                logger.info(f"GHL opportunity created: {result.get('id', '')} – {title}")
            return result
        except Exception as exc:
            logger.error(f"Error creating GHL opportunity: {exc}")
            return None

    async def move_opportunity_stage(
        self, opportunity_id: str, stage_id: str
    ) -> Optional[Dict]:
        """Move an opportunity to a different pipeline stage."""
        try:
            return await self._request(
                "PUT", f"/pipelines/opportunities/{opportunity_id}",
                json={"pipelineStageId": stage_id},
            )
        except Exception as exc:
            logger.error(f"Error moving GHL opportunity {opportunity_id}: {exc}")
            return None

    async def get_pipeline_opportunities(
        self, pipeline_id: Optional[str] = None
    ) -> List[Dict]:
        """Get all opportunities in a pipeline."""
        pid = pipeline_id or self.pipeline_id
        try:
            result = await self._request(
                "GET", "/pipelines/opportunities",
                params={"pipelineId": pid, "locationId": self.location_id},
            )
            return result.get("opportunities", []) if result else []
        except Exception as exc:
            logger.error(f"Error fetching GHL pipeline opportunities: {exc}")
            return []

    # ------------------------------------------------------------------
    # Calendar / Appointments
    # ------------------------------------------------------------------

    async def get_calendar_slots(
        self, start_date: str, end_date: str, calendar_id: Optional[str] = None
    ) -> List[Dict]:
        """Get available calendar slots."""
        cid = calendar_id or self.calendar_id
        try:
            result = await self._request(
                "GET", f"/calendars/{cid}/free-slots",
                params={"startDate": start_date, "endDate": end_date},
            )
            return result.get("slots", []) if result else []
        except Exception as exc:
            logger.error(f"Error fetching GHL calendar slots: {exc}")
            return []

    async def create_appointment(
        self,
        contact_id: str,
        start_time: str,
        end_time: str,
        title: str = "Consultation",
        calendar_id: Optional[str] = None,
    ) -> Optional[Dict]:
        """Book an appointment on the GHL calendar."""
        cid = calendar_id or self.calendar_id
        payload = {
            "calendarId": cid,
            "locationId": self.location_id,
            "contactId": contact_id,
            "startTime": start_time,
            "endTime": end_time,
            "title": title,
            "appointmentStatus": "confirmed",
        }
        try:
            result = await self._request("POST", "/calendars/events", json=payload)
            if result:
                logger.info(f"GHL appointment created for contact {contact_id}")
            return result
        except Exception as exc:
            logger.error(f"Error creating GHL appointment: {exc}")
            return None

    # ------------------------------------------------------------------
    # SMS & Conversations
    # ------------------------------------------------------------------

    async def send_sms(
        self, contact_id: str, message: str
    ) -> Optional[Dict]:
        """Send an SMS to a contact via GHL conversations."""
        payload = {
            "type": "SMS",
            "contactId": contact_id,
            "message": message,
        }
        try:
            result = await self._request(
                "POST", "/conversations/messages", json=payload
            )
            if result:
                logger.info(f"GHL SMS sent to contact {contact_id}")
            return result
        except Exception as exc:
            logger.error(f"Error sending GHL SMS: {exc}")
            return None

    # ------------------------------------------------------------------
    # Notes
    # ------------------------------------------------------------------

    async def add_note(
        self, contact_id: str, body: str
    ) -> Optional[Dict]:
        """Add a note to a contact."""
        try:
            return await self._request(
                "POST", f"/contacts/{contact_id}/notes",
                json={"body": body},
            )
        except Exception as exc:
            logger.error(f"Error adding GHL note: {exc}")
            return None

    # ------------------------------------------------------------------
    # High-level helpers
    # ------------------------------------------------------------------

    async def sync_lead(
        self,
        name: str,
        email: str = "",
        phone: str = "",
        company: str = "",
        source: str = "AI Agent",
    ) -> Optional[Dict]:
        """Convenience: create contact + opportunity in 'New Lead' stage."""
        parts = name.split(" ", 1)
        first = parts[0]
        last = parts[1] if len(parts) > 1 else ""

        contact_result = await self.create_contact(
            first_name=first,
            last_name=last,
            email=email,
            phone=phone,
            company=company,
            tags=[source, "AI-Qualified"],
        )
        if not contact_result:
            return None

        contact = contact_result.get("contact", contact_result)
        contact_id = contact.get("id")

        opp = await self.create_opportunity(
            contact_id=contact_id,
            title=f"{name} – {company or 'Direct'}",
            stage_id=self.stage_new,
        )

        return {
            "contact_id": contact_id,
            "opportunity": opp,
        }

    async def mark_booked(self, opportunity_id: str) -> Optional[Dict]:
        """Move opportunity to 'Booked' stage."""
        return await self.move_opportunity_stage(opportunity_id, self.stage_booked)


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------

_ghl_service: Optional[GoHighLevelService] = None


def get_ghl_service() -> GoHighLevelService:
    global _ghl_service
    if _ghl_service is None:
        _ghl_service = GoHighLevelService()
    return _ghl_service
