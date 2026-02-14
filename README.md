# Pilot (MVP scaffold)

Pilot is a self-hosted dashcam project focused on reliability, local ownership, and simple extensibility.

## MVP implemented in this scaffold

- Segment-oriented recording pipeline with deterministic naming.
- Segment metadata files containing device ID, UTC timestamp, and segment index.
- Retention management that keeps recent segments and preserves locked clips.
- Manual lock helper that marks a segment metadata file as locked.
- Offload command planner for rsync/SFTP/SMB methods.
- Single TOML configuration file (`config/pilot.toml`).

> Note: actual camera capture and boot-time system integration are intentionally out of scope in this initial scaffold and can be wired into `RecordingController` and deployment scripts.

## Module boundaries

- `pilot.config`: load and validate single config source.
- `pilot.recording`: segment naming and recording adapter.
- `pilot.metadata`: metadata schema and persistence.
- `pilot.storage`: retention + lock semantics.
- `pilot.offload`: transfer strategy planning.
- `pilot.service`: orchestration entry point for periodic ticks.
- `pilot.cli`: minimal CLI for local validation.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m pilot.cli --config config/pilot.toml --segments 3
pytest
```

## Future extensions

- Replace placeholder recording with ffmpeg/libcamera integration.
- Add systemd unit for power-on startup and graceful stop.
- Add optional local web UI for clip review/download.
- Add Wi-Fi trust detector feeding offload scheduler.
