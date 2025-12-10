# ScheduleSync
An automated tool that scans your Gmail inbox for emails from specific senders, detects scheduled activities, and syncs them into Google Calendar and Google Sheets.

## What’s here
- Streamlit entrypoint: `app.py`
- Core orchestration and parsing: `core/`
- Google integrations: `integrations/`
- Local data (settings, tokens, processed IDs): `data/`
- Sample settings: `data/settings.example.json`

## Quick start
1) Install dependencies (inside your virtualenv):
   ```bash
   pip install -r requirements.txt
   ```
2) Create your Google OAuth credentials (`credentials.json`) via Google Cloud Console and place it at `data/credentials.json`.
3) Copy `data/settings.example.json` to `data/settings.json` and edit senders, calendar ID, and sheet ID.
4) Run Streamlit:
   ```bash
   streamlit run app.py
   ```
5) Click "Run sync now" to trigger the Gmail → Calendar/Sheets flow. The first run will prompt OAuth and cache tokens in `data/token.json`.

## Notes
- The current integrations are stubbed to keep the scaffold runnable; wire up the actual Gmail/Calendar/Sheets calls where indicated.
- Processed email IDs are stored in `data/processed_ids.json` to avoid duplicate event creation.
