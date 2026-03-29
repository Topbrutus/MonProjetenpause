from __future__ import annotations

import argparse
from pathlib import Path
import sys

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from src.local_queue import LocalQueue
    from src.message_bus import MessageBus
    from src.run_controller import RunController
    from src.run_models import QueueResult
    from src.session import ParallelSession
else:
    from .local_queue import LocalQueue
    from .message_bus import MessageBus
    from .run_controller import RunController
    from .run_models import QueueResult
    from .session import ParallelSession


def build_controller() -> RunController:
    session = ParallelSession(session_id="run-local-queue")
    bus = MessageBus()
    queue = LocalQueue()
    return RunController(session=session, bus=bus, queue=queue)


def main() -> None:
    parser = argparse.ArgumentParser(description="RUN queue bridge for MonDeuxiemeProjet")
    parser.add_argument("command", nargs="*", help="Explicit RUN command to enqueue")
    parser.add_argument("--complete", dest="complete", help="Command id to complete")
    parser.add_argument("--target", dest="target", default="monprogramme")
    parser.add_argument("--status", dest="status", default="done")
    parser.add_argument("--detail", dest="detail", default="Traitement terminé.")
    args = parser.parse_args()

    controller = build_controller()

    if args.complete:
        payload = QueueResult(
            command_id=args.complete,
            target=args.target,
            status=args.status,
            detail=args.detail,
        )
        feedback = controller.complete(payload)
        print(feedback["monitor_text"])
        return

    raw_command = " ".join(args.command).strip()
    if not raw_command:
        parser.error("Provide a RUN command, for example: dispatch monprogramme start")

    feedback = controller.handle(raw_command)
    print(feedback["monitor_text"])
    print(f"Commande écrite dans: {feedback['queue_path']}")


if __name__ == "__main__":
    main()
