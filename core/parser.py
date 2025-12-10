from datetime import datetime, timedelta
from typing import Optional

import dateparser

from .models import Event


def parse_email(subject: str, body: str, sender: str | None = None, message_id: str | None = None) -> Optional[Event]:
    text_blob = f"{subject}\n{body}"
    parsed_dt = dateparser.parse(text_blob, settings={"PREFER_DATES_FROM": "future"})
    if not parsed_dt:
        return None

    start = parsed_dt
    end = start + timedelta(hours=1)
    title = subject.strip() or "Scheduled activity"
    return Event(
        title=title,
        start=start,
        end=end,
        description=body[:240],
        sender=sender,
        message_id=message_id,
        snippet=body[:120],
    )
