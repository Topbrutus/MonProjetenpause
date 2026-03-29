from __future__ import annotations

import json
from pathlib import Path

from .run_models import QueueResult, RunCommand


class LocalQueue:
    """Simple JSON file queue for command/result exchange with a local program."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or Path(".runtime")).resolve()
        self.commands_dir = self.root / "commands"
        self.results_dir = self.root / "results"
        self.logs_dir = self.root / "logs"
        self._ensure_layout()

    def _ensure_layout(self) -> None:
        for directory in (self.root, self.commands_dir, self.results_dir, self.logs_dir):
            directory.mkdir(parents=True, exist_ok=True)

    def enqueue(self, command: RunCommand) -> Path:
        destination = self.commands_dir / f"{command.command_id}.json"
        destination.write_text(
            json.dumps(command.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return destination

    def write_result(self, result: QueueResult) -> Path:
        destination = self.results_dir / f"{result.command_id}.json"
        destination.write_text(
            json.dumps(result.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return destination

    def read_result(self, command_id: str) -> QueueResult | None:
        source = self.results_dir / f"{command_id}.json"
        if not source.exists():
            return None
        data = json.loads(source.read_text(encoding="utf-8"))
        return QueueResult(
            command_id=str(data.get("command_id", command_id)),
            target=str(data.get("target", "")),
            status=str(data.get("status", "unknown")),
            detail=str(data.get("detail", "")),
            created_at=str(data.get("created_at", "")),
        )
