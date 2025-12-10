from __future__ import annotations

from typing import Optional

from googleapiclient.discovery import build

from core.models import Event
from .google_auth import load_credentials

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def get_client():
    creds = load_credentials(SCOPES)
    return build("calendar", "v3", credentials=creds)


def create_event(service, event: Event, calendar_id: str = "primary") -> Optional[str]:
    # Placeholder payload; real implementation should map timezone-aware datetimes.
    body = {
        "summary": event.title,
        "location": event.location,
        "description": event.description,
        "start": {"dateTime": event.start.isoformat()},
        "end": {"dateTime": event.end.isoformat()},
    }
    _ = service  # silence unused for now
    # In a full implementation: response = service.events().insert(calendarId=calendar_id, body=body).execute()
    # return response.get("id")
    return None
