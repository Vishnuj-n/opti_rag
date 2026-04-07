# Product Requirements: Opti RAG Environment

## What We Are Building

We are building a CPU-only, OpenEnv-compatible RAG optimization environment that lets an external agent tune retrieval settings and receive a deterministic reward per step.

The environment must:

- expose step-based RL-style APIs over HTTP
- execute real RAG retrieval with local embedding models and FAISS
- call a generation model through the Hugging Face Inference Router
- return a normalized reward in [0.0, 1.0] on every step

## Primary Goal

Enable repeatable evaluation of RAG parameter choices so an optimization policy can improve answer quality under realistic latency constraints.

## In Scope

- OpenEnv-style environment server and schemas
- RAG pipeline with chunking, embedding, indexing, retrieval, and answer generation
- deterministic local reward computation
- benchmark task set for reset/step evaluation
- Dockerized runtime suitable for Hugging Face Spaces

## Out of Scope

- GPU-only runtime requirements
- paid OpenAI API dependency
- Gym or Stable Baselines3 runtime/training dependency
- non-deterministic external judge as the primary reward source

## Required API Contract

The service must expose and support:

- POST /reset
- POST /step
- GET /state

Behavior requirements:

- /reset initializes a valid first state immediately
- /step accepts an action with embedding_model, chunk_size, and top_k
- /step returns observation, reward, done, and info-compatible fields
- /state returns the latest environment snapshot

## Required Build Artifacts

The project deliverable must include:

- openenv.yaml
- server/Dockerfile
- server/app.py
- models.py
- embedding.py
- setup_models.py
- root-level inference.py

## Inference and Model Routing Requirements

- generation calls must use Hugging Face Inference Router
- authentication must be via HF_TOKEN
- OpenAI-compatible SDK usage is allowed only when pointed to HF router base URL
- runtime must not require OPENAI_API_KEY

## Retrieval and Action Space Requirements

The optimization action must control these RAG parameters:

- embedding_model
- chunk_size
- top_k

Retrieval pipeline requirements:

- local embedding generation using sentence-transformers models
- FAISS index-based similarity retrieval
- retrieved context must be used in answer generation

## Reward Requirements

For every step:

- reward type must be float
- reward must be clamped to [0.0, 1.0]
- reward must be computed programmatically and deterministically

Reward design target:

- quality component from expected-vs-generated overlap
- coverage component from expected-vs-retrieved-context overlap
- latency penalty applied before final clamp

## Logging Requirements

root-level inference.py must print exactly these markers:

- [START] once at run start
- [STEP] once per step
- [END] once at run completion

## Runtime and Dependency Requirements

- Python 3.11+
- fastapi
- uvicorn
- faiss-cpu
- sentence-transformers
- openenv-core[cli]
- openai (only for HF router compatible client usage)
- requests
- numpy
- pyyaml

Runtime constraints:

- CPU-only execution path
- no Gym/Stable Baselines3 dependency in runtime path

## Local Embedding Models

The local setup and Docker image must support these models:

- sentence-transformers/all-MiniLM-L6-v2
- sentence-transformers/all-mpnet-base-v2
- nomic-ai/nomic-embed-text-v1.5

These models are for local embedding/retrieval only.

## Benchmark Data Requirements

tasks/tasks.json must define at least three benchmark tasks that include:

- short factual query
- long contextual query
- edge-case or abstention-sensitive query

## Acceptance Criteria (Definition of Done)

The build is complete only when all of the following are true:

- Docker image builds successfully from server/Dockerfile
- /reset, /step, and /state all pass smoke tests
- /step rewards are always float values in [0.0, 1.0]
- inference.py runs end-to-end with HF_TOKEN and no paid OpenAI key
- inference.py output preserves strict [START], [STEP], [END] format
- environment is deployable and runnable on Hugging Face Spaces
