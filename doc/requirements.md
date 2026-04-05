# Requirements

## Functional Requirements

- The environment must be defined using OpenEnv-compatible server patterns and schema models.
- The service must expose `POST /reset`, `POST /step`, and `GET /state`.
- The project must include `openenv.yaml`.
- The project must include `Dockerfile`.
- The project must include `inference.py` at the repository root.
- LLM inference must use the Hugging Face Inference Router, optionally through an OpenAI-compatible SDK, authenticated with `HF_TOKEN`.
- The runtime must not require a paid OpenAI API key.
- The service must run on CPU only.
- The grader must return a normalized float reward in the closed interval `[0.0, 1.0]` for every step.
- The use case must optimize real RAG parameters: `embedding_model`, `chunk_size`, and `top_k`.
- `inference.py` must print logs exactly in the `[START]`, `[STEP]`, `[END]` format.

## Environment Requirements

- Python 3.11 or newer.
- `fastapi`
- `uvicorn`
- `faiss-cpu`
- `sentence-transformers`
- `openenv-core[cli]`
- `openai` (SDK usage is allowed only when targeting the HF router endpoint)
- `requests`
- `numpy`
- `pyyaml`
- `einops`

## Local Model Requirements

- `sentence-transformers/all-MiniLM-L6-v2`
- `sentence-transformers/all-mpnet-base-v2`
- `nomic-ai/nomic-embed-text-v1.5`

These models are used only for local embedding and retrieval.

## Data Requirements

- `tasks/tasks.json` must define at least 3 benchmark tasks.
- The tasks must include:
- a short factual query
- a long contextual query
- an edge-case query

## Validation Requirements

- `/reset` returns a valid initial state immediately.
- `/step` accepts a valid action payload.
- `GET /state` reflects the latest environment state.
- `inference.py` runs without format drift.
- `inference.py` succeeds when configured with HF router variables and no `OPENAI_API_KEY`.
- Reward values are validated as float and clamped to `[0.0, 1.0]`.
- Runtime path contains no Gym or Stable Baselines3 dependency.
- Docker image builds successfully.
- The project is deployable to Hugging Face Spaces.
