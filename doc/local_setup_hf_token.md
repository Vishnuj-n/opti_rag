# Local Setup Guide: Hugging Face Token

## Goal

Run the project locally on CPU using Hugging Face Inference Router authentication.

## Prerequisites

- Python 3.11+
- Project virtual environment activated
- A Hugging Face token with inference access

## Required Environment Variables

Set these variables before running the server or inference script:

- `HF_TOKEN`: Hugging Face access token
- `API_BASE_URL`: Hugging Face Inference Router base URL
- `MODEL_NAME`: Inference model identifier

PowerShell example:

```powershell
$env:HF_TOKEN = "hf_xxx"
$env:API_BASE_URL = "https://router.huggingface.co/v1"
$env:MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"
```

## Compliance Notes

- No paid OpenAI API key is required.
- If `OPENAI_API_KEY` exists in your shell profile, unset it for compliance testing.

PowerShell example:

```powershell
Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue
```

## Quick Local Check

1. Start the API server.
2. Run `inference.py`.
3. Confirm logs print in `[START]`, `[STEP]`, `[END]` format.
4. Confirm successful run with only HF-based variables.
