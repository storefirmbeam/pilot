from __future__ import annotations

from datetime import datetime, timezone, timedelta
from pathlib import Path


class RetentionManager:
    def __init__(self, output_dir: Path, retention_hours: int) -> None:
        self.output_dir = output_dir
        self.retention = timedelta(hours=retention_hours)

    def enforce(self, now: datetime | None = None) -> list[Path]:
        now = now or datetime.now(tz=timezone.utc)
        deleted: list[Path] = []

        for meta in sorted(self.output_dir.glob("*.json")):
            if self._is_locked(meta):
                continue
            stamp = datetime.fromtimestamp(meta.stat().st_mtime, tz=timezone.utc)
            if now - stamp <= self.retention:
                continue

            video = meta.with_suffix(".mp4")
            if video.exists():
                video.unlink()
                deleted.append(video)
            meta.unlink()
            deleted.append(meta)

        return deleted

    @staticmethod
    def _is_locked(meta_file: Path) -> bool:
        return '"locked": true' in meta_file.read_text(encoding="utf-8").lower()


def lock_segment(meta_file: Path) -> None:
    text = meta_file.read_text(encoding="utf-8")
    if '"locked": false' in text:
        meta_file.write_text(text.replace('"locked": false', '"locked": true'), encoding="utf-8")
