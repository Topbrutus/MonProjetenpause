from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class RunCommand:
    command_id: str
    raw_text: str
    action: str
    target: str
    args: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now_iso)
    status: str = "queued"

    @classmethod
    def create(cls, raw_text: str, action: str, target: str, args: list[str]) -> "RunCommand":
        return cls(
            command_id=str(uuid4()),
            raw_text=raw_text,
            action=action,
            target=target,
            args=list(args),
        )

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class QueueResult:
    command_id: str
    target: str
    status: str
    detail: str
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
