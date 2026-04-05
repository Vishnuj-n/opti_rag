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

3. Run locally (optional verification):

```bash
uv run python server/opti_rag_environment.py
uv run uvicorn server.app:app --reload
```

## OpenEnv Integration (Final Step)

1. Copy environment:

`<project>/opti_rag` -> `<OpenEnv_repo>/envs/opti_rag_env`

2. Build:

```bash
docker build -t opti_rag_env:latest -f envs/opti_rag_env/server/Dockerfile .
```
