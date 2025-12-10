from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Iterable, List, Sequence

from googleapiclient.discovery import build

from .google_auth import load_credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


@dataclass
class GmailMessage:
    id: str
    subject: str
    body: str
    sender: str


def get_client():
    creds = load_credentials(SCOPES)
    return build("gmail", "v1", credentials=creds)


def build_query(senders: Sequence[str], since: datetime | None = None) -> str:
    parts: List[str] = []
    if senders:
        senders_clause = " OR ".join(f"from:{s}" for s in senders)
        parts.append(f"({senders_clause})")
    if since:
        parts.append(f"newer_than:{(datetime.utcnow() - since).days}d")
    return " ".join(parts)


def fetch_new_emails(
    service,
    senders: Sequence[str],
    since: datetime,
    processed_checker: Callable[[str], bool],
) -> Iterable[GmailMessage]:
    query = build_query(senders, since)
    # Placeholder: in a full implementation, iterate messages via Gmail API.
    # Returning an empty list keeps the skeleton runnable without credentials.
    _ = (service, query, processed_checker)  # appease linters for now
    return []
