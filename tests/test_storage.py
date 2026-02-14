from datetime import datetime, timezone, timedelta
from pathlib import Path
import os

from pilot.storage import RetentionManager, lock_segment


def _touch(path: Path, seconds_old: int) -> None:
    path.touch()
    old = (datetime.now(tz=timezone.utc) - timedelta(seconds=seconds_old)).timestamp()
    os.utime(path, (old, old))


def test_retention_deletes_old_unlocked(tmp_path: Path) -> None:
    video = tmp_path / "a.mp4"
    meta = tmp_path / "a.json"
    _touch(video, seconds_old=7200)
    meta.write_text('{"locked": false}', encoding="utf-8")
    old = (datetime.now(tz=timezone.utc) - timedelta(seconds=7200)).timestamp()
    os.utime(meta, (old, old))

    removed = RetentionManager(tmp_path, retention_hours=1).enforce()
    assert video in removed
    assert meta in removed
    assert not video.exists()
    assert not meta.exists()


def test_retention_keeps_locked(tmp_path: Path) -> None:
    video = tmp_path / "b.mp4"
    meta = tmp_path / "b.json"
    _touch(video, seconds_old=7200)
    meta.write_text('{"locked": false}', encoding="utf-8")
    lock_segment(meta)

    removed = RetentionManager(tmp_path, retention_hours=1).enforce()
    assert removed == []
    assert video.exists()
    assert meta.exists()
