from pathlib import Path

from pilot.config import load_config


def test_load_config(tmp_path: Path) -> None:
    cfg = tmp_path / "pilot.toml"
    cfg.write_text(
        """
[recording]
output_dir = "segments"
segment_seconds = 120
retention_hours = 48
device_id = "abc"

[offload]
enabled = true
trusted_ssids = ["A", "B"]
method = "rsync"
target = "nas:/clips"
""",
        encoding="utf-8",
    )

    loaded = load_config(cfg)
    assert loaded.recording.output_dir == Path("segments")
    assert loaded.recording.segment_seconds == 120
    assert loaded.recording.retention_hours == 48
    assert loaded.offload.enabled is True
    assert loaded.offload.trusted_ssids == ["A", "B"]
