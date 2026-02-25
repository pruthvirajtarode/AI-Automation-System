"""
Airtable Integration Service
Syncs leads, tasks, and bookings to Airtable bases for reporting and collaboration.
"""

import logging
from typing import Dict, List, Optional

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

AIRTABLE_API = "https://api.airtable.com/v0"


class AirtableService:
    """Handles Airtable read/write via the REST API."""

    def __init__(self):
        self.token = settings.AIRTABLE_TOKEN
        self._configured = bool(self.token)

        if not self._configured:
            logger.warning("Airtable service not configured – token missing.")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def _request(
        self, method: str, url: str, json: Optional[Dict] = None, params: Optional[Dict] = None
    ) -> Optional[Dict]:
        if not self._configured:
            return None

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.request(
                method, url, headers=self._headers(), json=json, params=params
            )
            resp.raise_for_status()
            return resp.json()

    # ------------------------------------------------------------------
    # Bases
    # ------------------------------------------------------------------

    async def list_bases(self) -> List[Dict]:
        """List all accessible Airtable bases."""
        try:
            result = await self._request("GET", "https://api.airtable.com/v0/meta/bases")
            return result.get("bases", []) if result else []
        except Exception as exc:
            logger.error(f"Error listing Airtable bases: {exc}")
            return []

    # ------------------------------------------------------------------
    # Records
    # ------------------------------------------------------------------

    async def list_records(
        self, base_id: str, table_name: str, max_records: int = 100
    ) -> List[Dict]:
        """List records from a table."""
        try:
            result = await self._request(
                "GET",
                f"{AIRTABLE_API}/{base_id}/{table_name}",
                params={"maxRecords": str(max_records)},
            )
            return result.get("records", []) if result else []
        except Exception as exc:
            logger.error(f"Error listing Airtable records: {exc}")
            return []

    async def create_record(
        self, base_id: str, table_name: str, fields: Dict
    ) -> Optional[Dict]:
        """Create a record in a table."""
        try:
            result = await self._request(
                "POST",
                f"{AIRTABLE_API}/{base_id}/{table_name}",
                json={"fields": fields},
            )
            if result:
                logger.info(f"Airtable record created in {table_name}: {result.get('id')}")
            return result
        except Exception as exc:
            logger.error(f"Error creating Airtable record: {exc}")
            return None

    async def update_record(
        self, base_id: str, table_name: str, record_id: str, fields: Dict
    ) -> Optional[Dict]:
        """Update a record."""
        try:
            return await self._request(
                "PATCH",
                f"{AIRTABLE_API}/{base_id}/{table_name}/{record_id}",
                json={"fields": fields},
            )
        except Exception as exc:
            logger.error(f"Error updating Airtable record: {exc}")
            return None

    async def delete_record(
        self, base_id: str, table_name: str, record_id: str
    ) -> bool:
        """Delete a record."""
        try:
            await self._request(
                "DELETE", f"{AIRTABLE_API}/{base_id}/{table_name}/{record_id}"
            )
            return True
        except Exception as exc:
            logger.error(f"Error deleting Airtable record: {exc}")
            return False

    # ------------------------------------------------------------------
    # High-level helpers
    # ------------------------------------------------------------------

    async def sync_lead(
        self,
        base_id: str,
        table_name: str,
        lead_data: Dict,
    ) -> Optional[Dict]:
        """Push a lead record to Airtable for tracking / reporting."""
        fields = {
            "Name": lead_data.get("name", ""),
            "Email": lead_data.get("email", ""),
            "Phone": lead_data.get("phone", ""),
            "Company": lead_data.get("company", ""),
            "Status": lead_data.get("status", "new"),
            "Score": lead_data.get("quality_score", 0),
            "Source": lead_data.get("source", "AI Agent"),
        }
        return await self.create_record(base_id, table_name, fields)


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------

_airtable_service: Optional[AirtableService] = None


def get_airtable_service() -> AirtableService:
    global _airtable_service
    if _airtable_service is None:
        _airtable_service = AirtableService()
    return _airtable_service
