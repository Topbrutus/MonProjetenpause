from dataclasses import dataclass

from .message_bus import MessageBus
from .session import ParallelSession


@dataclass(slots=True)
class Orchestrator:
    session: ParallelSession
    bus: MessageBus

    def run_wave(self, prompts_by_agent: dict[str, str], category: str = "wave") -> int:
        turn = self.session.next_turn()
        for agent, content in prompts_by_agent.items():
            if agent not in self.session.agents:
                self.session.register_agent(agent)
            self.bus.publish(
                agent=agent,
                content=content,
                turn=turn,
                category=category,
            )
        return turn

    def transcript(self) -> str:
        lines: list[str] = [
            "# DEMO — Conversation parallèle entre GPT",
            "",
            f"Session: {self.session.session_id}",
            f"Participants: {', '.join(self.session.agents) if self.session.agents else 'aucun'}",
            f"Tours joués: {self.session.current_turn}",
        ]

        for turn in range(1, self.session.current_turn + 1):
            messages = self.bus.by_turn(turn)
            lines.extend(
                [
                    "",
                    f"## Tour {turn}",
                    f"Vague parallèle: {len(messages)} messages",
                    "",
                ]
            )
            for index, message in enumerate(messages, start=1):
                lines.append(
                    f"{index}. [{message.agent}] ({message.category}) {message.content}"
                )

        if self.session.current_turn:
            lines.extend(
                [
                    "",
                    "## Synthèse",
                    f"La session a produit {self.session.current_turn} tours et {len(self.bus._messages)} messages.",
                    "Chaque tour représente une vague où plusieurs agents parlent dans la même fenêtre logique.",
                ]
            )

        return "\n".join(lines)
