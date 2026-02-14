from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .metadata import SegmentMetadata, write_metadata


@dataclass(slots=True)
class SegmentPaths:
    video: Path
    metadata: Path


class SegmentNamer:
    def __init__(self, output_dir: Path, device_id: str) -> None:
        self.output_dir = output_dir
        self.device_id = device_id

    def build(self, segment_index: int, started_at: datetime | None = None) -> SegmentPaths:
        started_at = started_at or datetime.now(tz=timezone.utc)
        stamp = started_at.strftime("%Y%m%dT%H%M%SZ")
        stem = f"{self.device_id}_{stamp}_{segment_index:06d}"
        return SegmentPaths(
            video=self.output_dir / f"{stem}.mp4",
            metadata=self.output_dir / f"{stem}.json",
        )


class RecordingController:
    """Recording adapter that currently creates placeholders for segment files."""

    def __init__(self, output_dir: Path, device_id: str) -> None:
        self.output_dir = output_dir
        self.device_id = device_id
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def finalize_segment(self, segment_index: int) -> SegmentPaths:
        paths = SegmentNamer(self.output_dir, self.device_id).build(segment_index)
        paths.video.touch()
        write_metadata(
            paths.metadata,
            SegmentMetadata(
                device_id=self.device_id,
                segment_index=segment_index,
                started_at=datetime.now(tz=timezone.utc),
            ),
        )
        return paths
