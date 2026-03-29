from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ParsedCommand:
    action: str
    target: str
    args: list[str]


class RunRouter:
    """Parse explicit RUN commands without relying on an LLM."""

    _ALIASES: dict[str, str] = {
        "run": "start",
        "start": "start",
        "stop": "stop",
        "status": "status",
        "dispatch": "dispatch",
        "send": "dispatch",
        "open": "open",
    }

    def parse(self, raw_text: str) -> ParsedCommand:
        clean = " ".join(raw_text.strip().split())
        if not clean:
            raise ValueError("Commande vide.")

        tokens = clean.split(" ")
        action_token = tokens[0].lower()
        action = self._ALIASES.get(action_token)
        if action is None:
            raise ValueError(
                "Commande inconnue. Utilise start/run, stop, status, dispatch/send ou open."
            )

        if len(tokens) < 2:
            raise ValueError("Une cible est requise. Exemple: dispatch monprogramme start")

        target = tokens[1].strip().lower()
        if not target:
            raise ValueError("La cible ne peut pas être vide.")

        args = [token for token in tokens[2:] if token.strip()]
        return ParsedCommand(action=action, target=target, args=args)
