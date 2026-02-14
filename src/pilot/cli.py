from __future__ import annotations

import argparse

from .config import load_config
from .service import PilotService


def main() -> None:
    parser = argparse.ArgumentParser(description="Pilot dashcam service")
    parser.add_argument("--config", default="config/pilot.toml")
    parser.add_argument("--segments", type=int, default=1)
    args = parser.parse_args()

    config = load_config(args.config)
    service = PilotService(config)
    for i in range(args.segments):
        service.tick(i)


if __name__ == "__main__":
    main()
