from pathlib import Path
import sys

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from src.message_bus import MessageBus
    from src.orchestrator import Orchestrator
    from src.session import ParallelSession
else:
    from .message_bus import MessageBus
    from .orchestrator import Orchestrator
    from .session import ParallelSession


def build_demo() -> str:
    session = ParallelSession(session_id="demo-parallel-gpt")
    bus = MessageBus()
    orchestrator = Orchestrator(session=session, bus=bus)

    first_turn = orchestrator.run_wave(
        {
            "Run": "J'ouvre le tour et je fixe l'objectif commun.",
            "Rex": "Je propose la structure technique minimale pour la conversation parallèle.",
        },
        category="seed-wave",
    )

    orchestrator.run_dependent_wave(
        {
            "Rio": "Après lecture du tour {source_turn}, je valide la cohérence suivante : {context}",
            "Rune": "Après lecture du tour {source_turn}, je prépare le chemin d'exécution suivant : {context}",
        },
        source_turn=first_turn,
        category="dependent-review",
    )

    orchestrator.run_dependent_wave(
        {
            "Run": "Je résume ce qui ressort du tour {source_turn} et j'annonce la suite : {context}",
        },
        category="orchestrator-summary",
    )

    return orchestrator.transcript()


def main() -> None:
    print(build_demo())


if __name__ == "__main__":
    main()
