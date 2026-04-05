---
title: Opti Rag Environment Server
emoji: 🏑
colorFrom: purple
colorTo: yellow
sdk: docker
pinned: false
app_port: 8000
base_path: /web
tags:
  - openenv
---

# Opti Rag Environment

A minimal OpenEnv-compatible environment for Opti RAG.

## Quick Start

1. Create virtual environment:

```bash
uv venv
```

2. Install dependencies:

```bash
uv sync
```

3. Warm up local embedding models (one-time, recommended):

```bash
uv run python setup_models.py
```

This script pre-downloads and caches the three embedding models used by the environment, printing progress like:
- `installing model 1/3: sentence-transformers/all-MiniLM-L6-v2`
- `installed and cached: sentence-transformers/all-MiniLM-L6-v2`

4. Run locally (optional verification):

```bash
uv run python server.opti_rag_environment.py
uv run uvicorn server.app:app --reload
```

## OpenEnv Integration (Final Step)

1. Copy environment:

`<project>/opti_rag` -> `<OpenEnv_repo>/envs/opti_rag_env`

2. Build:

```bash
docker build -t opti_rag_env:latest -f envs/opti_rag_env/server/Dockerfile .
```

The Docker image build runs `setup_models.py`, so embedding models are cached in-image and available at startup without first-step downloads.

> If building from the local repository, ensure `.dockerignore` excludes local virtual environments such as `.venv/` so the build context does not include invalid local Python environments.
