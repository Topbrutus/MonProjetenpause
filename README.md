# MonDeuxiemeProjet

MonDeuxiemeProjet est le nouveau projet centré sur une capacité absente du premier projet : permettre à plusieurs GPT de parler en parallèle dans un cadre structuré.

## Objectif

Construire une base technique et conceptuelle pour :

- faire converser plusieurs GPT en parallèle ;
- garder une trace claire des messages, tours et rôles ;
- préparer une orchestration où plusieurs agents peuvent parler sans se marcher dessus ;
- rendre ce comportement testable, extensible et documenté.

## Vision initiale

Le projet vise une architecture simple en plusieurs couches :

1. **Session** : représente une conversation parallèle active.
2. **Message bus** : transporte et enregistre les messages entre agents.
3. **Orchestrateur** : décide quels agents parlent, quand et selon quelles règles.
4. **Entrée principale** : lance une démonstration ou un futur mode réel.

## État actuel

Initialisation du projet en cours.

## Structure actuelle

- `PROJECT-BACKLOG.md` : plan de travail du projet
- `ARCHITECTURE.md` : architecture cible et règles de circulation des messages
- `src/session.py` : modèle de session parallèle
- `src/message_bus.py` : bus de messages local
- `src/orchestrator.py` : orchestration des prises de parole
- `src/main.py` : point d'entrée de démonstration
- `.gitignore` : exclusions locales Python

## Première démonstration prévue

La première démonstration doit montrer qu'une session peut :

1. enregistrer plusieurs agents ;
2. faire circuler des messages structurés ;
3. exécuter plusieurs tours ;
4. produire une sortie lisible de la conversation parallèle.

## Prochaine étape logique

Valider la structure de base, puis brancher une vraie stratégie de tours parallèles et des règles anti-collision de parole.


## Lancer la démo

```bash
python src/main.py
```

La sortie attendue est une transcription lisible d'une session où plusieurs agents publient dans les mêmes tours.
