import json
from pathlib import Path
from typing import Iterable, Set

from .config import DATA_DIR, ensure_data_dir


class ProcessedStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or DATA_DIR / "processed_ids.json"
        ensure_data_dir(self.path.parent)
        self._ids: Set[str] = set()
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text())
            self._ids = set(data)
        except json.JSONDecodeError:
            self._ids = set()

    def _persist(self) -> None:
        self.path.write_text(json.dumps(sorted(self._ids), indent=2))

    def has(self, message_id: str) -> bool:
        return message_id in self._ids

    def add(self, message_id: str) -> None:
        self._ids.add(message_id)
        self._persist()

    def bulk_add(self, message_ids: Iterable[str]) -> None:
        self._ids.update(message_ids)
        self._persist()
