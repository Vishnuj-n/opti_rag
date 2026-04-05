# Sprint Plan: RL / OpenEnv RAG Optimizer

## Sprint Goal

Ship a hackathon-ready RAG optimization environment that:

- runs on Hugging Face Spaces
- exposes `/reset`, `/step`, and `/state`
- includes `openenv.yaml`, `Dockerfile`, and root `inference.py`
- uses local embeddings and FAISS for retrieval
- uses the Hugging Face Inference Router for LLM calls (OpenAI-compatible SDK allowed)
- prints strict `[START]`, `[STEP]`, `[END]` logs in `inference.py`

## Current Build Status

- Done: project skeleton created
- Done: `main.py` FastAPI API created
- Done: `server/app.py` added for OpenEnv-style layout
- Done: `openenv.yaml` added
- Done: `models.py` with OpenEnv-compatible action/observation/state models
- Done: `env.py` environment logic added
- Done: `rag.py` local RAG pipeline added
- Done: `embedding.py` local embedding loader added
- Done: `tasks/tasks.json` with 3 benchmark tasks added
- Done: `Dockerfile` added
- Done: root `inference.py` added
- Done: local OpenEnv structure validation passed
- In progress: runtime validation with the repo environment
- Pending: full endpoint smoke test
- Pending: reward quality tuning after runtime smoke test

## Sprint Backlog

### Sprint 1: Submission Skeleton

- [x] Create required repo structure
- [x] Add FastAPI backend
- [x] Add OpenEnv metadata and server layout
- [x] Add benchmark tasks and local corpus
- [x] Add inference script and Dockerfile

### Sprint 2: Runtime Validation

- [ ] Verify imports using the repo interpreter
- [ ] Verify `/reset` returns a valid initial state
- [ ] Verify `/step` accepts valid actions
- [ ] Verify `/state` reflects latest environment state
- [ ] Verify `inference.py` runs without crashing
- [ ] Verify `inference.py` runs with `HF_TOKEN` and no paid OpenAI key
- [ ] Verify reward value type is float and always in `[0.0, 1.0]`

### Sprint 3: Submission Hardening

- [ ] Confirm rewards stay in `[0, 1]`
- [ ] Confirm logs match the required format exactly
- [ ] Confirm Docker image builds cleanly
- [ ] Confirm Space ping and health behavior
- [ ] Confirm no heavy downloads happen at runtime
- [ ] Remove any Gym or Stable Baselines3 dependency from runtime path
- [ ] Run OpenEnv CLI init/validate flow and archive output as submission evidence
- [ ] Add compliance matrix mapping every hackathon constraint to code/docs

## Known Blockers

### Local Runtime Dependency Gap

The current workspace interpreter check failed on:

`ModuleNotFoundError: No module named 'faiss'`

What this means:

- the code structure is in place
- the local OpenEnv validator passes
- the repo Python environment still needs the FAISS runtime available for true end-to-end testing in this workspace

This does not change the intended submission architecture, but it does block final local runtime verification until resolved.

## How Quality Score Is Computed

The scorer is intentionally local and deterministic so it stays within hackathon constraints:

- answer overlap score: token-level F1 between expected answer and produced answer
- context coverage score: token-level F1 between expected answer and retrieved context
- abstention handling: edge-case tasks reward a correct “I do not know based on the provided context.” response
- final quality score: `0.65 * answer_overlap + 0.35 * context_coverage`
- latency penalty: `min(latency_seconds / 8.0, 0.25)`
- reward: `clamp(quality_score - latency_penalty, 0.0, 1.0)`

This avoids using an external LLM judge for scoring while still keeping the reward meaningful.

## Files To Review

- `main.py`
- `server/app.py`
- `models.py`
- `env.py`
- `rag.py`
- `embedding.py`
- `inference.py`
- `openenv.yaml`
- `Dockerfile`
- `tasks/tasks.json`

## Next Immediate Steps

1. Resolve the local FAISS runtime availability.
2. Run end-to-end API smoke tests.
3. Run `inference.py` and verify the exact output format.
4. Tighten any reward or response-shape issues that show up in smoke tests.
