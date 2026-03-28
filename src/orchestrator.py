from dataclasses import dataclass

from .message_bus import Message, MessageBus
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

    def run_dependent_wave(
        self,
        templates_by_agent: dict[str, str],
        source_turn: int | None = None,
        category: str = "dependent-reply",
    ) -> int:
        default_turn = self.session.current_turn
        target_turn = source_turn or default_turn
        source_messages = self.bus.by_turn(target_turn)
        context = self._messages_to_context(source_messages)
        dependent_prompts: dict[str, str] = {}

        for agent, template in templates_by_agent.items():
            dependent_prompts[agent] = template.format(
                context=context,
                source_turn=target_turn,
            )

        return self.run_wave(dependent_prompts, category=category)

    def _messages_to_context(self, messages: list[Message]) -> str:
        if not messages:
            return "Aucun message source."

        return " | ".join(
            f"{message.agent}: {message.content}" for message in messages
        )

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
            categories = sorted({message.category for message in messages})

            lines.extend(
                [
                    "",
                    f"## Tour {turn}",
                    f"Catégories: {', '.join(categories)}" if categories else "Catégorie : inconnue",
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
                    "Le mode dépendant montre qu'un agent peut attendre et même se baser sur la vague précédente avant de répondre.",
                ]
            )

        return "\n".join(lines)
