from __future__ import annotations

from typing import Optional

from googleapiclient.discovery import build

from core.models import Event
from .google_auth import load_credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_client():
    creds = load_credentials(SCOPES)
    return build("sheets", "v4", credentials=creds)


def append_event_row(service, event: Event, calendar_event_id: Optional[str], sheet_id: str) -> None:
    row = [
        event.title,
        event.start.isoformat(),
        event.end.isoformat(),
        event.location or "",
        event.sender or "",
        calendar_event_id or "",
        event.message_id or "",
    ]
    _ = (service, sheet_id, row)  # silence unused for now
    # In a full implementation: service.spreadsheets().values().append(...).execute()
