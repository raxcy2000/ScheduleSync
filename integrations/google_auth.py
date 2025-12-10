from __future__ import annotations

from pathlib import Path
from typing import Sequence

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from core.config import DATA_DIR

TOKEN_PATH = DATA_DIR / "token.json"
CREDENTIALS_PATH = DATA_DIR / "credentials.json"


def load_credentials(scopes: Sequence[str]) -> Credentials:
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, scopes)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_PATH.write_text(creds.to_json())
        return creds

    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), scopes=scopes)
    creds = flow.run_local_server(port=0)
    TOKEN_PATH.write_text(creds.to_json())
    return creds
