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

    orchestrator.run_wave(
        {
            "Run": "J'ouvre le tour et je fixe l'objectif commun.",
            "Rex": "Je propose la structure technique minimale pour la conversation parallèle.",
            "Rio": "Je vérifie déjà la lisibilité et la cohérence de la base.",
        }
    )

    orchestrator.run_wave(
        {
            "Run": "Nous pouvons maintenant clarifier les règles de prise de parole.",
            "Rex": "Le bus et l'orchestrateur sont prêts à évoluer vers de vraies interactions.",
            "Rio": "La démo reste simple, mais elle montre bien la logique par vagues.",
        }
    )

    orchestrator.run_wave(
        {
            "Run": "Prochaine étape: brancher de vrais agents ou une stratégie plus riche.",
            "Rex": "On pourra ensuite ajouter priorités, files et filtres.",
            "Rio": "La sortie finale est maintenant lisible comme démonstration du parallélisme.",
        },
        category="summary",
    )

    return orchestrator.transcript()


def main() -> None:
    print(build_demo())


if __name__ == "__main__":
    main()
