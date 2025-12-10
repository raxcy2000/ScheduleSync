from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationError


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SETTINGS_PATH = DATA_DIR / "settings.json"


class Settings(BaseModel):
    senders: List[str] = Field(default_factory=list)
    calendar_id: str = "primary"
    sheet_id: str = ""
    default_event_duration_minutes: int = 60
    lookback_days: int = 7
    timezone: str = "UTC"
    description_template: str = "Source: {sender}\\nSummary: {snippet}"


def ensure_data_dir(path: Optional[Path] = None) -> Path:
    data_dir = path or DATA_DIR
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def load_settings(path: Optional[Path] = None) -> Settings:
    settings_path = path or SETTINGS_PATH
    ensure_data_dir(settings_path.parent)
    if not settings_path.exists():
        return Settings()
    with settings_path.open() as f:
        payload = json.load(f)
    try:
        return Settings(**payload)
    except ValidationError as exc:
        raise ValueError(f"Invalid settings file at {settings_path}") from exc


def save_settings(settings: Settings, path: Optional[Path] = None) -> None:
    settings_path = path or SETTINGS_PATH
    ensure_data_dir(settings_path.parent)
    settings_path.write_text(settings.json(indent=2))
