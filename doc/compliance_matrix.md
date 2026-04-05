# Hackathon Compliance Matrix

| Constraint | Requirement | Evidence Location | Status |
|---|---|---|---|
| Framework | Environment defined with OpenEnv (no Gym/SB3 runtime path) | `openenv.yaml`, `server/app.py`, `models.py`, `doc/requirements.md` | In progress |
| Agent | LLM agent evaluated via `inference.py`, not PPO training | `inference.py`, `doc/architecture.md`, `doc/requirements.md` | In progress |
| Reward | Programmatic grader returns normalized float in `[0.0, 1.0]` | `env.py`, `rag.py`, `doc/requirements.md` | In progress |
| Execution | Runs locally on CPU without paid OpenAI key | `doc/local_setup_hf_token.md`, `doc/requirements.md` | In progress |
| Structure | OpenEnv layout with models and server API | `models.py`, `server/app.py`, `openenv.yaml`, `doc/architecture.md` | In progress |
| Use Case | Real-world RAG parameter optimization task | `rag.py`, `tasks/tasks.json`, `doc/architecture.md` | In progress |

## How To Finalize

1. Replace each `In progress` with `Pass` after local verification.
2. Attach command outputs from smoke tests and `inference.py` runs.
3. Record any known limitations in the sprint blocker section.
