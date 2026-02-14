from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shlex


@dataclass(slots=True)
class OffloadPlan:
    command: list[str]


class OffloadPlanner:
    def __init__(self, method: str, target: str) -> None:
        self.method = method
        self.target = target

    def build(self, source_dir: Path) -> OffloadPlan:
        src = str(source_dir) + "/"
        if self.method == "rsync":
            return OffloadPlan(["rsync", "-av", "--ignore-existing", src, self.target])
        if self.method == "sftp":
            return OffloadPlan(["sftp", self.target])
        if self.method == "smb":
            return OffloadPlan(["smbclient", self.target, "-c", f"recurse on; prompt off; mput {shlex.quote(src)}*"])
        raise ValueError(f"unsupported offload method: {self.method}")
