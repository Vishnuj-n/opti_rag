"""Local embedding helpers for CPU-only, offline-friendly execution."""

from __future__ import annotations

import os
from typing import Dict

from sentence_transformers import SentenceTransformer

# Canonical model names used throughout the project.
MODEL_MAP = {
    "MiniLM": "sentence-transformers/all-MiniLM-L6-v2",
    "nomic-v1.5": "nomic-ai/nomic-embed-text-v1.5",
    "mpnet": "sentence-transformers/all-mpnet-base-v2",
    # Allow direct names as aliases too.
    "all-MiniLM-L6-v2": "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-MiniLM-L6-v2": "sentence-transformers/all-MiniLM-L6-v2",
    "nomic-ai/nomic-embed-text-v1.5": "nomic-ai/nomic-embed-text-v1.5",
    "all-mpnet-base-v2": "sentence-transformers/all-mpnet-base-v2",
    "sentence-transformers/all-mpnet-base-v2": "sentence-transformers/all-mpnet-base-v2",
}

_model_cache: Dict[str, SentenceTransformer] = {}


def _cache_folder() -> str | None:
    return os.getenv("SENTENCE_TRANSFORMERS_HOME")


def _allow_download(default: bool = False) -> bool:
    raw = os.getenv("EMBEDDING_ALLOW_DOWNLOAD")
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def _needs_trust_remote_code(model_name: str) -> bool:
    return model_name.startswith("nomic-ai/")


def _load_model(full_model_name: str, allow_download: bool) -> SentenceTransformer:
    cache_folder = _cache_folder()
    local_only = not allow_download
    try:
        return SentenceTransformer(
            full_model_name,
            cache_folder=cache_folder,
            local_files_only=local_only,
            trust_remote_code=_needs_trust_remote_code(full_model_name),
        )
    except OSError as exc:
        if local_only:
            raise RuntimeError(
                f"Model '{full_model_name}' was not found in local cache. "
                "Run `python setup_models.py` before starting the environment."
            ) from exc
        raise


def get_embedding(text: str, model_alias: str, allow_download: bool | None = None) -> list[float]:
    full_model_name = MODEL_MAP.get(model_alias)
    if full_model_name is None:
        supported = ", ".join(sorted({"MiniLM", "nomic-v1.5", "mpnet"}))
        raise ValueError(f"Unknown model alias '{model_alias}'. Supported: {supported}")

    effective_allow_download = _allow_download(default=False) if allow_download is None else allow_download

    if full_model_name not in _model_cache:
        _model_cache[full_model_name] = _load_model(
            full_model_name, allow_download=effective_allow_download
        )

    embedding = _model_cache[full_model_name].encode(text)
    return embedding.tolist()
