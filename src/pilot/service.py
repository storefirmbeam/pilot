from __future__ import annotations

from pathlib import Path

from .config import PilotConfig
from .offload import OffloadPlanner
from .recording import RecordingController
from .storage import RetentionManager


class PilotService:
    """Minimal service orchestrator for MVP modules."""

    def __init__(self, config: PilotConfig) -> None:
        self.config = config
        out = Path(config.recording.output_dir)
        self.recorder = RecordingController(out, config.recording.device_id)
        self.retention = RetentionManager(out, config.recording.retention_hours)
        self.offload = OffloadPlanner(config.offload.method, config.offload.target)

    def tick(self, segment_index: int) -> None:
        self.recorder.finalize_segment(segment_index)
        self.retention.enforce()
