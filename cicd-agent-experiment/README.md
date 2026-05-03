# A Comparative Study of Multi-Agent Generative Pipelines for Automated CI/CD Failure Diagnosis, Root Cause Analysis, and Remediation

This repository contains a small, deterministic Python simulation for comparing CI/CD debugging configurations in a graduate research project on Generative Intelligence and Software Development Lifecycles.

The project models agentic CI/CD failure diagnosis without calling external LLM APIs. Instead, it uses readable rule-based logic to simulate how different generative pipeline structures may affect diagnosis, remediation, consistency, and reliability.

## Research Question

To what extent does a structured multi-agent generative pipeline improve the accuracy, consistency, and reliability of CI/CD failure diagnosis and remediation compared to a single-agent LLM approach?

## Repository Structure

```text
cicd-agent-experiment/
├── README.md
├── requirements.txt
├── main.py
├── scenarios.py
├── agents.py
├── evaluator.py
└── results/
    └── .gitkeep
```

## Experimental Configurations

The experiment compares three configurations:

1. **Single-Agent Baseline**: A one-pass agent diagnoses the log and recommends a fix.
2. **Multi-Agent Pipeline Without Validation**: Separate agents handle log processing, root cause analysis, and fix recommendation.
3. **Multi-Agent Pipeline With Validation**: The structured multi-agent pipeline adds a validation stage that checks whether the evidence, root cause, and fix are aligned.

## Scenarios

The controlled benchmark includes five representative CI/CD failures:

- Missing Python dependency: `ModuleNotFoundError: No module named 'requests'`
- Unit test assertion failure: `AssertionError: Expected 5 but got 3`
- Missing environment variable: `KeyError: 'API_KEY'`
- Docker build path error: `COPY failed: file not found`
- GitHub Actions workflow configuration error: invalid workflow file / unexpected value

Each scenario includes an expected failure type, expected root cause, and expected fix keywords.

## Evaluation Metrics

Each configuration is evaluated using scores of `1.0`, `0.5`, or `0.0`.

- **Diagnostic Accuracy**: Compares predicted failure type and root cause against expected scenario data.
- **Fix Correctness**: Checks whether the recommended fix contains relevant expected remediation keywords.
- **Consistency**: Assigns deterministic consistency scores based on the structure of each configuration.
- **Reasoning Quality**: Scores whether the output clearly connects log evidence to root cause and recommended fix.
- **Overall Reliability**: Average of diagnostic accuracy, fix correctness, consistency, and reasoning quality.

## How to Run

From the repository directory:

```bash
pip install -r requirements.txt
python main.py
```

The script prints an aggregate results table to the terminal and exports:

```text
results/experiment_results.csv
```

## Expected Output

The terminal output includes a table similar to:

```text
Configuration                  | Diagnostic Accuracy | Fix Correctness | Consistency | Reasoning Quality | Overall Reliability
-------------------------------+---------------------+-----------------+-------------+-------------------+--------------------
Single-Agent Baseline          | 0.90                | 1.00            | 0.50        | 0.50              | 0.72
Multi-Agent Without Validation | 1.00                | 1.00            | 0.75        | 1.00              | 0.94
Multi-Agent With Validation    | 1.00                | 1.00            | 1.00        | 1.00              | 1.00
```

Exact values may change if the scenario set or scoring rules are modified.

## Research Use

The generated CSV can be imported into a spreadsheet, notebook, or plotting tool to create tables and charts for the final report. Because the simulation is deterministic, repeated runs produce the same results, which makes the experiment easy to reproduce and explain.

## Important Note

This is a controlled research simulation. The agents use rule-based logic to model generative pipeline behavior and architectural differences between single-agent and multi-agent approaches. No external LLM APIs, credentials, or network calls are used.
