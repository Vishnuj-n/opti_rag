# Evaluation Instructions

## Local CPU Evaluation

### 1. Start the environment server

Run the project API locally.

Example:

```powershell
uv run main.py
```

If your project uses uvicorn directly:

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Configure inference variables

Set:

- `HF_TOKEN`
- `API_BASE_URL`
- `MODEL_NAME`

Ensure `OPENAI_API_KEY` is not required.

### 3. Run the evaluation agent

```powershell
python inference.py
```

### 4. Validate required output format

The script output must include:

- `[START]` once at run start
- `[STEP]` for each action step
- `[END]` once at run completion

### 5. Validate reward constraints

For each step response:

- reward type is float
- reward value is in `[0.0, 1.0]`

### 6. Validate OpenEnv interface

Confirm these endpoints operate correctly:

- `POST /reset`
- `POST /step`
- `GET /state`

## Optional Submission Evidence

Capture and save:

- terminal output from `inference.py`
- endpoint smoke test results
- OpenEnv CLI validation output
