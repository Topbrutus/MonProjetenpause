from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(slots=True)
class Message:
    message_id: str
    agent: str
    content: str
    turn: int
    category: str
    created_at: str


class MessageBus:
    def __init__(self) -> None:
        self._messages: list[Message] = []

    def publish(self, agent: str, content: str, turn: int, category: str = "chat") -> Message:
        message = Message(
            message_id=str(uuid4()),
            agent=agent,
            content=content,
            turn=turn,
            category=category,
            created_at=datetime.now(UTC).isoformat(),
        )
        self._messages.append(message)
        return message

    def by_turn(self, turn: int) -> list[Message]:
        return [message for message in self._messages if message.turn == turn]
