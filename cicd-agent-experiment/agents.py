"""Rule-based agent simulations for CI/CD failure diagnosis."""


def _detect_failure(log: str) -> dict:
    """Extract a failure type and key evidence from a raw CI/CD log."""
    normalized = log.lower()

    if "modulenotfounderror" in normalized and "requests" in normalized:
        return {
            "failure_type": "missing_dependency",
            "evidence": "ModuleNotFoundError: No module named 'requests'",
        }
    if "assertionerror" in normalized:
        return {
            "failure_type": "test_assertion_failure",
            "evidence": "AssertionError indicates observed behavior did not match the expected test result.",
        }
    if "keyerror" in normalized and "api_key" in normalized:
        return {
            "failure_type": "missing_environment_variable",
            "evidence": "KeyError: 'API_KEY'",
        }
    if "copy failed" in normalized and "file not found" in normalized:
        return {
            "failure_type": "docker_build_path_error",
            "evidence": "COPY failed: file not found in build context.",
        }
    if "invalid workflow file" in normalized or "unexpected value" in normalized:
        return {
            "failure_type": "workflow_configuration_error",
            "evidence": "Invalid workflow file with an unexpected value.",
        }

    return {
        "failure_type": "unknown_failure",
        "evidence": "No known CI/CD failure pattern matched.",
    }


def single_agent_baseline(log: str) -> dict:
    """Simulate a single agent that diagnoses and recommends a fix in one pass."""
    detected = _detect_failure(log)
    failure_type = detected["failure_type"]

    if failure_type == "missing_dependency":
        root_cause = "A Python package is missing from the CI environment."
        fix = "Install requests with pip install requests and add it to requirements.txt."
    elif failure_type == "test_assertion_failure":
        root_cause = "A unit test assertion failed because the result differed from the expected value."
        fix = "Review the assertion and update the implementation or test expectation."
    elif failure_type == "missing_environment_variable":
        root_cause = "A required environment variable is not configured."
        fix = "Add API_KEY as a CI environment secret."
    elif failure_type == "docker_build_path_error":
        root_cause = "The Docker build cannot find a file referenced by COPY."
        fix = "Check the Dockerfile COPY path and build context."
    elif failure_type == "workflow_configuration_error":
        root_cause = "The CI workflow YAML contains an invalid field."
        fix = "Review the GitHub Actions workflow YAML near the unexpected value."
    else:
        root_cause = "The failure pattern is unclear."
        fix = "Inspect the CI log manually."

    return {
        "failure_type": failure_type,
        "evidence": detected["evidence"],
        "root_cause": root_cause,
        "recommended_fix": fix,
        "reasoning": "Single-pass diagnosis based on the most visible error message.",
        "final_status": "completed",
    }


def log_processing_agent(log: str) -> dict:
    """Extract structured evidence from the raw CI/CD log."""
    detected = _detect_failure(log)
    return {
        "failure_type": detected["failure_type"],
        "evidence": detected["evidence"],
        "raw_log_excerpt": log.splitlines()[-1] if log.splitlines() else log,
        "reasoning": "The log was normalized and matched against known CI/CD failure signatures.",
    }


def root_cause_analysis_agent(summary: dict) -> dict:
    """Map extracted log evidence to a likely root cause."""
    failure_type = summary["failure_type"]

    root_causes = {
        "missing_dependency": "The requests package is imported but not installed in the CI environment.",
        "test_assertion_failure": "The tested function returned a value that does not satisfy the assertion.",
        "missing_environment_variable": "The CI job does not provide the required API_KEY environment variable.",
        "docker_build_path_error": "The Dockerfile COPY instruction references a path missing from the build context.",
        "workflow_configuration_error": "The GitHub Actions workflow contains an unsupported or misplaced key.",
    }

    return {
        "failure_type": failure_type,
        "evidence": summary.get("evidence", ""),
        "root_cause": root_causes.get(failure_type, "The root cause could not be determined."),
        "reasoning": (
            "The extracted evidence was connected to the most likely CI/CD configuration, "
            "test, dependency, or build cause."
        ),
    }


def fix_recommendation_agent(root_cause: dict) -> dict:
    """Generate a remediation recommendation from a diagnosed root cause."""
    failure_type = root_cause["failure_type"]

    fixes = {
        "missing_dependency": (
            "Add requests to requirements.txt and ensure the workflow runs pip install -r requirements.txt."
        ),
        "test_assertion_failure": (
            "Inspect the failing assertion, then correct the implementation or update the test expectation."
        ),
        "missing_environment_variable": (
            "Define API_KEY as a GitHub Actions secret or environment variable and pass it to the job."
        ),
        "docker_build_path_error": (
            "Update the Dockerfile COPY path or build context so the referenced file exists during docker build."
        ),
        "workflow_configuration_error": (
            "Fix the GitHub Actions workflow YAML by moving or renaming the unexpected value according to the schema."
        ),
    }

    return {
        "failure_type": failure_type,
        "recommended_fix": fixes.get(failure_type, "Manually inspect the failing CI/CD step."),
        "reasoning": "The fix targets the diagnosed root cause rather than only the visible symptom.",
    }


def validation_agent(summary: dict, root_cause: dict, fix: dict) -> dict:
    """Validate whether evidence, root cause, and fix are aligned."""
    aligned = (
        summary.get("failure_type") == root_cause.get("failure_type")
        and root_cause.get("failure_type") == fix.get("failure_type")
        and bool(summary.get("evidence"))
        and bool(root_cause.get("root_cause"))
        and bool(fix.get("recommended_fix"))
    )

    return {
        "validation_result": "passed" if aligned else "failed",
        "final_status": "validated" if aligned else "needs_review",
        "reasoning": (
            "Validation checked that the same failure type appears across extraction, "
            "root cause analysis, and remediation."
        ),
    }


def run_multi_agent_without_validation(log: str) -> dict:
    """Run the structured multi-agent pipeline without a validation stage."""
    summary = log_processing_agent(log)
    root_cause = root_cause_analysis_agent(summary)
    fix = fix_recommendation_agent(root_cause)

    return {
        "failure_type": summary["failure_type"],
        "evidence": summary["evidence"],
        "root_cause": root_cause["root_cause"],
        "recommended_fix": fix["recommended_fix"],
        "reasoning": (
            f"{summary['reasoning']} {root_cause['reasoning']} {fix['reasoning']}"
        ),
        "final_status": "completed",
    }


def run_multi_agent_with_validation(log: str) -> dict:
    """Run the structured multi-agent pipeline with validation."""
    summary = log_processing_agent(log)
    root_cause = root_cause_analysis_agent(summary)
    fix = fix_recommendation_agent(root_cause)
    validation = validation_agent(summary, root_cause, fix)

    return {
        "failure_type": summary["failure_type"],
        "evidence": summary["evidence"],
        "root_cause": root_cause["root_cause"],
        "recommended_fix": fix["recommended_fix"],
        "reasoning": (
            f"{summary['reasoning']} {root_cause['reasoning']} "
            f"{fix['reasoning']} {validation['reasoning']}"
        ),
        "validation_result": validation["validation_result"],
        "final_status": validation["final_status"],
    }
