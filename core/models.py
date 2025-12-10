from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Event:
    title: str
    start: datetime
    end: datetime
    location: Optional[str] = None
    description: Optional[str] = None
    sender: Optional[str] = None
    message_id: Optional[str] = None
    snippet: Optional[str] = None
