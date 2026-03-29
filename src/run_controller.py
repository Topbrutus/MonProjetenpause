from __future__ import annotations

import json
from pathlib import Path

from .local_queue import LocalQueue
from .message_bus import MessageBus
from .run_models import QueueResult, RunCommand
from .run_router import ParsedCommand, RunRouter
from .session import ParallelSession


class RunController:
    """Route explicit RUN commands toward the local queue and keep a trace."""

    def __init__(
        self,
        *,
        session: ParallelSession,
        bus: MessageBus,
        queue: LocalQueue | None = None,
        events_path: Path | None = None,
        task_board_path: Path | None = None,
    ) -> None:
        self.session = session
        self.bus = bus
        self.router = RunRouter()
        self.queue = queue or LocalQueue()
        self.events_path = events_path or (self.queue.logs_dir / "events.jsonl")
        self.task_board_path = task_board_path or (self.queue.logs_dir / "task_board.json")
        self._ensure_task_board()

    def handle(self, raw_text: str) -> dict[str, object]:
        parsed = self.router.parse(raw_text)
        command = RunCommand.create(
            raw_text=raw_text,
            action=parsed.action,
            target=parsed.target,
            args=parsed.args,
        )

        turn = self.session.next_turn()
        if "Run" not in self.session.agents:
            self.session.register_agent("Run")

        self.bus.publish(
            agent="Run",
            content=self._render_bus_content(parsed),
            turn=turn,
            category="run-command",
        )
        self.queue.enqueue(command)
        self._append_event(command, turn=turn, kind="queued")
        self._append_task(command)

        return {
            "turn": turn,
            "command": command.to_dict(),
            "queue_path": str(self.queue.commands_dir / f"{command.command_id}.json"),
            "monitor_text": self._render_monitor_feedback(command),
        }

    def complete(self, result: QueueResult) -> dict[str, object]:
        self.queue.write_result(result)
        self._append_event(result, turn=self.session.current_turn, kind="result")
        self._update_task_status(result.command_id, result.status)
        return {
            "result": result.to_dict(),
            "monitor_text": f"Résultat {result.status} pour {result.target}: {result.detail}",
        }

    def _render_bus_content(self, parsed: ParsedCommand) -> str:
        tail = f" {' '.join(parsed.args)}" if parsed.args else ""
        return f"{parsed.action} {parsed.target}{tail}".strip()

    def _render_monitor_feedback(self, command: RunCommand) -> str:
        args = " ".join(command.args).strip()
        suffix = f" | args: {args}" if args else ""
        return (
            f"Commande RUN en file: {command.action} -> {command.target}"
            f"{suffix} | id={command.command_id}"
        )

    def _append_event(self, payload: RunCommand | QueueResult, *, turn: int, kind: str) -> None:
        event = {
            "kind": kind,
            "turn": turn,
            "created_at": getattr(payload, "created_at", ""),
            "payload": payload.to_dict(),
        }
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")

    def _ensure_task_board(self) -> None:
        if self.task_board_path.exists():
            return
        board = {"todo": [], "doing": [], "review": [], "done": []}
        self.task_board_path.write_text(
            json.dumps(board, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _append_task(self, command: RunCommand) -> None:
        board = json.loads(self.task_board_path.read_text(encoding="utf-8"))
        board.setdefault("todo", []).append(
            {
                "command_id": command.command_id,
                "target": command.target,
                "action": command.action,
                "args": command.args,
                "status": command.status,
            }
        )
        self.task_board_path.write_text(
            json.dumps(board, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _update_task_status(self, command_id: str, status: str) -> None:
        board = json.loads(self.task_board_path.read_text(encoding="utf-8"))
        columns = ("todo", "doing", "review", "done")
        found = None
        for column in columns:
            tasks = board.get(column, [])
            for index, task in enumerate(tasks):
                if task.get("command_id") == command_id:
                    found = tasks.pop(index)
                    break
            if found is not None:
                break

        if found is None:
            found = {"command_id": command_id"}

        found["status"] = status
        destination = "done" if status in {"done", "ok", "success"} else "review"
        board.setdefault(destination, []).append(found)
        self.task_board_path.write_text(
            json.dumps(board, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
