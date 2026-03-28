# ARCHITECTURE

## Goal
Allow multiple GPT-style agents to talk in the same session.

## Core parts
- session: keeps agents and turn count
- bus: stores messages
- orchestrator: opens a turn and collects agent outputs

## First mode
Wave-based parallelism:
1. open a turn
2. several agents publish in the same turn
3. store all messages
4. move to next turn
