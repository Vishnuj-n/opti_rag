"""One-time local model warm-up for CPU-only embedding workflows."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from sentence_transformers import SentenceTransformer

MODELS = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "nomic-ai/nomic-embed-text-v1.5",
    "sentence-transformers/all-mpnet-base-v2",
]


def _needs_trust_remote_code(model_name: str) -> bool:
    return model_name.startswith("nomic-ai/")


def download_models(cache_dir: str | None = None, offline_only: bool = False) -> None:
    total_models = len(MODELS)
    for index, model_name in enumerate(MODELS, start=1):
        print(
            f"[setup_models] installing model {index}/{total_models}: {model_name} "
            "(downloading or loading from cache)"
        )
        SentenceTransformer(
            model_name,
            cache_folder=cache_dir,
            local_files_only=offline_only,
            trust_remote_code=_needs_trust_remote_code(model_name),
        )
        print(f"[setup_models] installed and cached: {model_name}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pre-download embedding models.")
    parser.add_argument(
        "--cache-dir",
        default=os.getenv("SENTENCE_TRANSFORMERS_HOME"),
        help="Target cache directory. Defaults to SENTENCE_TRANSFORMERS_HOME.",
    )
    parser.add_argument(
        "--offline-only",
        action="store_true",
        help="Fail instead of downloading if the model is not already cached.",
    )
    args = parser.parse_args()

    cache_dir = args.cache_dir
    if cache_dir:
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        print(f"[setup_models] cache dir: {cache_dir}")

    download_models(cache_dir=cache_dir, offline_only=args.offline_only)


if __name__ == "__main__":
    main()
