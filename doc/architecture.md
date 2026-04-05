# Architecture

## Overview

This project is an OpenEnv-compatible RAG optimization service built around a FastAPI backend.
It exposes the required `/reset`, `/step`, and `/state` endpoints, while also providing OpenEnv-style
`models.py`, `server/app.py`, and `openenv.yaml` files for hackathon packaging.

## Main Components

- `main.py`: public FastAPI app used by the submission surface.
- `server/app.py`: OpenEnv-style server entry point built with `openenv.core.env_server.http_server.create_app`.
- `models.py`: Pydantic action, observation, and state models.
- `env.py`: environment state machine and reward wiring.
- `rag.py`: document chunking, FAISS retrieval, answer generation, and reward scoring.
- `embedding.py`: local embedding model loading and embedding generation.
- `inference.py`: strict log-format runner that drives the API through `/reset` and `/step`.
- `tasks/tasks.json`: benchmark tasks and local corpus used for grading.

## Request Flow

1. `POST /reset` initializes the environment with one of the local benchmark tasks.
2. `POST /step` accepts an action containing `embedding_model`, `chunk_size`, and `top_k`.
3. The environment chunks the corpus, embeds the chunks, builds or reuses a FAISS index, and retrieves top chunks.
4. LLM inference is executed by `inference.py` through the Hugging Face Inference Router using an OpenAI-compatible SDK pointed to the HF router base URL.
5. Reward is computed locally and normalized into `[0, 1]`.
6. `GET /state` returns the current observation/state snapshot.

## Reward Design

Reward is intentionally deterministic and local:

- `quality_score` is based on token-level F1 overlap between the expected answer and the produced answer.
- `context_coverage` measures how much of the expected answer is supported by the retrieved context.
- `latency_penalty` is derived from step latency and capped so the final reward stays in range.
- Final reward is `clamp(quality_score - latency_penalty, 0.0, 1.0)`.

This avoids external judge dependencies and keeps the service CPU-friendly.

## OpenEnv Compatibility

The repo includes the standard OpenEnv-style files expected by the validator:

- `openenv.yaml`
- `server/app.py`
- `models.py`

Environment definition contract:

- The RL environment is defined through OpenEnv-compatible server primitives and typed schemas in `models.py` for action, observation, and state.
- The serving layer exposes reset, step, and state through the OpenEnv API surface.
- No Gym or Stable Baselines3 training loop is used; the acting policy is an LLM evaluated through `inference.py`.

The project also keeps the FastAPI submission interface requested in the original hackathon brief:

- `/reset`
- `/step`
- `/state`
- `/health`
- `/metadata`

## Runtime Notes

- Embedding models are local-only.
- The Dockerfile preloads the embedding models during image build to reduce runtime downloads.
- The runtime path uses `HF_TOKEN` against the Hugging Face router endpoint and does not require a paid OpenAI API key.
- The current local workspace still needs `faiss` available in the active interpreter for full smoke testing.

