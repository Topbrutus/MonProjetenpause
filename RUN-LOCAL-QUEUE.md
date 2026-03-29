# RUN local queue bridge

This V1 adds a deterministic bridge between RUN and a local target program without relying on an external LLM.

## Goal

Allow Nino RUN or any future cockpit to send explicit commands toward a local program through JSON files.

## Flow

1. RUN receives an explicit command such as `dispatch monprogramme start`
2. `RunRouter` parses the command
3. `RunController` creates a `RunCommand`
4. The command is written into `.runtime/commands/<command_id>.json`
5. The local target program reads that file and executes the requested action
6. The target program writes a result into `.runtime/results/<command_id>.json`
7. `RunController.complete(...)` records the result and updates the local task board

## Supported command styles

- `run monprogramme`
- `start monprogramme`
- `stop monprogramme`
- `status monprogramme`
- `dispatch monprogramme build`
- `send monprogramme build`

## Local runtime files

- `.runtime/commands/` queued command payloads
- `.runtime/results/` returned result payloads
- `.runtime/logs/events.jsonl` event trace
- `.runtime/logs/task_board.json` simple local board

## Quick test

```bash
python src/run_cli.py dispatch monprogramme start
```

Then simulate the program response:

```bash
python src/run_cli.py --complete <command-id> --target monprogramme --status done --detail "Démarrage terminé."
```

## Why this shape

- deterministic
- easy to debug
- traceable
- compatible with a future hub/event registry model
- safe starting point before any direct external action
