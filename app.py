import streamlit as st

from core.config import Settings, load_settings, save_settings
from core.sync_manager import run_sync


def parse_sender_input(raw: str) -> list[str]:
    parts = [part.strip() for part in raw.replace(",", "\n").splitlines()]
    return [p for p in parts if p]


def settings_form(settings: Settings) -> Settings:
    st.subheader("Settings")
    with st.form("settings-form"):
        senders_raw = st.text_area("Senders (one per line)", "\n".join(settings.senders), height=120)
        calendar_id = st.text_input("Calendar ID", settings.calendar_id)
        sheet_id = st.text_input("Sheet ID or URL", settings.sheet_id)
        default_duration = st.number_input(
            "Default event duration (minutes)", min_value=15, max_value=240, value=settings.default_event_duration_minutes
        )
        lookback = st.number_input("Lookback days for Gmail search", min_value=1, max_value=30, value=settings.lookback_days)
        timezone = st.text_input("Timezone", settings.timezone)
        description_template = st.text_area("Description template", settings.description_template, height=80)
        submitted = st.form_submit_button("Save settings")

        if submitted:
            updated = Settings(
                senders=parse_sender_input(senders_raw),
                calendar_id=calendar_id,
                sheet_id=sheet_id,
                default_event_duration_minutes=int(default_duration),
                lookback_days=int(lookback),
                timezone=timezone,
                description_template=description_template,
            )
            save_settings(updated)
            st.success("Settings saved.")
            return updated
    return settings


def main() -> None:
    st.title("ScheduleSync")
    st.caption("Scan Gmail for events and sync them to Google Calendar + Sheets.")

    settings = load_settings()
    settings = settings_form(settings)

    if st.button("Run sync now"):
        with st.spinner("Syncing..."):
            summary = run_sync(settings)
        st.success(f"Synced {summary['events_created']} events from {summary['emails_scanned']} emails.")
        if summary["events"]:
            st.write("Created events")
            st.table(
                [
                    {
                        "Title": event.title,
                        "Start": event.start,
                        "End": event.end,
                        "Sender": event.sender,
                        "Location": event.location,
                    }
                    for event in summary["events"]
                ]
            )
    st.divider()
    st.info(
        "Place your Google API credentials at data/credentials.json. "
        "First run will prompt OAuth consent and store tokens in data/token.json."
    )


if __name__ == "__main__":
    main()
