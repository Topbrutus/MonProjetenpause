from .message_bus import MessageBus
from .orchestrator import Orchestrator
from .session import ParallelSession


def main() -> None:
    session = ParallelSession(session_id="demo-parallel-gpt")
    bus = MessageBus()
    orchestrator = Orchestrator(session=session, bus=bus)

    orchestrator.run_wave(
        {
            "Run": "I set the goal for this turn.",
            "Rex": "I propose a minimal technical structure.",
            "Rio": "I validate readability and coherence.",
        }
    )

    orchestrator.run_wave(
        {
            "Run": "We can now prepare a richer orchestration.",
            "Rex": "The session and bus are ready to evolve.",
            "Rio": "The current base stays simple and testable.",
        }
    )

    print(orchestrator.transcript())


if __name__ == "__main__":
    main()
