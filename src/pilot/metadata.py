from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path


@dataclass(slots=True)
class SegmentMetadata:
    device_id: str
    segment_index: int
    started_at: datetime
    locked: bool = False

    def to_json(self) -> str:
        payload = {
            "device_id": self.device_id,
            "segment_index": self.segment_index,
            "started_at": self.started_at.astimezone(timezone.utc).isoformat(),
            "locked": self.locked,
        }
        return json.dumps(payload, indent=2)


def write_metadata(path: Path, metadata: SegmentMetadata) -> None:
    path.write_text(metadata.to_json(), encoding="utf-8")
