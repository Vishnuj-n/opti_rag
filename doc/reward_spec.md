# Reward Specification

## Purpose

Define a deterministic, programmatic reward function for RAG optimization actions.

## Contract

For every environment step:

- reward type: `float`
- reward range: `[0.0, 1.0]`
- reward source: local programmatic grader only

## Inputs

- expected answer text
- generated answer text
- retrieved context text
- step latency in seconds

## Components

- answer overlap score: token-level F1(expected, generated)
- context coverage score: token-level F1(expected, retrieved_context)
- quality score: `0.65 * answer_overlap + 0.35 * context_coverage`
- latency penalty: `min(latency_seconds / 8.0, 0.25)`

## Final Reward

`reward = clamp(quality_score - latency_penalty, 0.0, 1.0)`

## Compliance Checks

- Validate reward is always cast to float.
- Validate clamping on every step before response serialization.
- Add tests for underflow and overflow paths.
