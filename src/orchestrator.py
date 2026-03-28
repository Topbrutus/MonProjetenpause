from dataclasses import dataclass

from .message_bus import MessageBus
from .session import ParallelSession


@dataclass(slots=True)
class Orchestrator:
    session: ParallelSession
    bus: MessageBus

    def run_wave(self, prompts_by_agent: dict[str, str]) -> int:
        turn = self.session.next_turn()
        for agent, content in prompts_by_agent.items():
            if agent not in self.session.agents:
                self.session.register_agent(agent)
            self.bus.publish(agent=agent, content=content, turn=turn)
        return turn

    def transcript(self) -> str:
        lines = [f"Session: {self.session.session_id}"]
        for turn in range(1, self.session.current_turn + 1):
            lines.append("")
            lines.append(f"## Turn {turn}")
            for message in self.bus.by_turn(turn):
                lines.append(f"- {message.agent}: {message.content}")
        return "\n".join(lines)
