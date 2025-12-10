from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List

from . import parser
from .config import Settings, load_settings
from .models import Event
from .storage import ProcessedStore
from integrations import calendar_client, gmail_client, sheets_client


def run_sync(settings: Settings | None = None) -> Dict[str, object]:
    settings = settings or load_settings()
    processed = ProcessedStore()

    gmail = gmail_client.get_client()
    calendar = calendar_client.get_client()
    sheets = sheets_client.get_client()

    since = datetime.utcnow() - timedelta(days=settings.lookback_days)
    messages = gmail_client.fetch_new_emails(
        gmail,
        senders=settings.senders,
        since=since,
        processed_checker=processed.has,
    )

    events: List[Event] = []
    for message in messages:
        event = parser.parse_email(
            subject=message.subject,
            body=message.body,
            sender=message.sender,
            message_id=message.id,
        )
        if not event:
            continue

        calendar_event_id = calendar_client.create_event(calendar, event, calendar_id=settings.calendar_id)
        sheets_client.append_event_row(sheets, event, calendar_event_id, settings.sheet_id)
        processed.add(message.id)
        events.append(event)

    return {
        "emails_scanned": len(messages),
        "events_created": len(events),
        "events": events,
    }
