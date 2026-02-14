from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]


@dataclass(slots=True)
class RecordingConfig:
    output_dir: Path
    segment_seconds: int
    retention_hours: int
    device_id: str


@dataclass(slots=True)
class OffloadConfig:
    enabled: bool
    trusted_ssids: list[str]
    method: str
    target: str


@dataclass(slots=True)
class PilotConfig:
    recording: RecordingConfig
    offload: OffloadConfig



def load_config(path: str | Path) -> PilotConfig:
    raw = tomllib.loads(Path(path).read_text(encoding="utf-8"))

    rec = raw["recording"]
    off = raw.get("offload", {})

    return PilotConfig(
        recording=RecordingConfig(
            output_dir=Path(rec["output_dir"]),
            segment_seconds=int(rec.get("segment_seconds", 60)),
            retention_hours=int(rec.get("retention_hours", 24)),
            device_id=str(rec.get("device_id", "pilot-001")),
        ),
        offload=OffloadConfig(
            enabled=bool(off.get("enabled", False)),
            trusted_ssids=list(off.get("trusted_ssids", [])),
            method=str(off.get("method", "rsync")),
            target=str(off.get("target", "")),
        ),
    )
