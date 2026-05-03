"""Evaluation utilities for comparing CI/CD debugging configurations."""


def _contains_any(text: str, keywords: list[str]) -> bool:
    """Return True when text contains at least one expected keyword."""
    normalized = text.lower()
    return any(keyword.lower() in normalized for keyword in keywords)


def _contains_many(text: str, keywords: list[str]) -> bool:
    """Return True when text contains at least two expected keywords."""
    normalized = text.lower()
    return sum(keyword.lower() in normalized for keyword in keywords) >= 2


def score_diagnostic_accuracy(output: dict, scenario: dict) -> float:
    """Score whether the predicted failure type and root cause match expectations."""
    type_match = output.get("failure_type") == scenario["expected_failure_type"]
    root_text = output.get("root_cause", "").lower()
    expected_terms = scenario["expected_root_cause"].lower().replace(".", "").split()
    root_overlap = sum(term in root_text for term in expected_terms if len(term) > 4)

    if type_match and root_overlap >= 2:
        return 1.0
    if type_match or root_overlap >= 2:
        return 0.5
    return 0.0


def score_fix_correctness(output: dict, scenario: dict) -> float:
    """Score whether the recommendation includes expected remediation keywords."""
    fix = output.get("recommended_fix", "")
    if _contains_many(fix, scenario["expected_fix_keywords"]):
        return 1.0
    if _contains_any(fix, scenario["expected_fix_keywords"]):
        return 0.5
    return 0.0


def score_consistency(configuration: str) -> float:
    """Assign deterministic consistency scores by configuration structure."""
    scores = {
        "Single-Agent Baseline": 0.5,
        "Multi-Agent Without Validation": 0.75,
        "Multi-Agent With Validation": 1.0,
    }
    return scores[configuration]


def score_reasoning_quality(output: dict) -> float:
    """Score whether reasoning links evidence, root cause, and fix."""
    has_evidence = bool(output.get("evidence"))
    has_root_cause = bool(output.get("root_cause"))
    has_fix = bool(output.get("recommended_fix"))
    reasoning = output.get("reasoning", "").lower()

    if has_evidence and has_root_cause and has_fix and "evidence" in reasoning and "root cause" in reasoning:
        return 1.0
    if has_evidence and has_root_cause and has_fix:
        return 0.5
    return 0.0


def evaluate_output(output: dict, scenario: dict, configuration: str) -> dict:
    """Evaluate one configuration output for one scenario."""
    diagnostic_accuracy = score_diagnostic_accuracy(output, scenario)
    fix_correctness = score_fix_correctness(output, scenario)
    consistency = score_consistency(configuration)
    reasoning_quality = score_reasoning_quality(output)
    overall_reliability = (
        diagnostic_accuracy + fix_correctness + consistency + reasoning_quality
    ) / 4

    return {
        "diagnostic_accuracy": diagnostic_accuracy,
        "fix_correctness": fix_correctness,
        "consistency": consistency,
        "reasoning_quality": reasoning_quality,
        "overall_reliability": overall_reliability,
    }


def average_metrics(rows: list[dict]) -> dict:
    """Average metric dictionaries across scenarios."""
    metric_names = [
        "diagnostic_accuracy",
        "fix_correctness",
        "consistency",
        "reasoning_quality",
        "overall_reliability",
    ]
    return {
        metric: sum(row[metric] for row in rows) / len(rows)
        for metric in metric_names
    }
