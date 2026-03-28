from dataclasses import dataclass, field


@dataclass(slots=True)
class ParallelSession:
    session_id: str
    agents: list[str] = field(default_factory=list)
    current_turn: int = 0

    def register_agent(self, agent_name: str) -> None:
        if agent_name not in self.agents:
            self.agents.append(agent_name)

    def next_turn(self) -> int:
        self.current_turn += 1
        return self.current_turn
