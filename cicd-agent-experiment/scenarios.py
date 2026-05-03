"""Representative CI/CD failure scenarios for the experiment."""

SCENARIOS = [
    {
        "id": "S1",
        "name": "Missing Python dependency",
        "raw_log": (
            "Run python -m pytest\n"
            "ImportError while importing test module 'tests/test_client.py'.\n"
            "ModuleNotFoundError: No module named 'requests'"
        ),
        "expected_failure_type": "missing_dependency",
        "expected_root_cause": "The requests package is imported but not installed in the CI environment.",
        "expected_fix_keywords": ["requests", "requirements.txt", "pip install"],
    },
    {
        "id": "S2",
        "name": "Unit test assertion failure",
        "raw_log": (
            "FAILED tests/test_calculator.py::test_add\n"
            "AssertionError: Expected 5 but got 3\n"
            "assert add(2, 3) == 5"
        ),
        "expected_failure_type": "test_assertion_failure",
        "expected_root_cause": "The tested function returned 3 instead of the expected value 5.",
        "expected_fix_keywords": ["assertion", "expected", "implementation", "test"],
    },
    {
        "id": "S3",
        "name": "Missing environment variable",
        "raw_log": (
            "Run python app.py\n"
            "File \"config.py\", line 8, in load_config\n"
            "KeyError: 'API_KEY'"
        ),
        "expected_failure_type": "missing_environment_variable",
        "expected_root_cause": "The CI job does not provide the required API_KEY environment variable.",
        "expected_fix_keywords": ["API_KEY", "environment", "secret", "GitHub Actions"],
    },
    {
        "id": "S4",
        "name": "Docker build path error",
        "raw_log": (
            "Step 4/8 : COPY ./service/requirements.txt /app/requirements.txt\n"
            "COPY failed: file not found in build context or excluded by .dockerignore: "
            "stat service/requirements.txt: file does not exist"
        ),
        "expected_failure_type": "docker_build_path_error",
        "expected_root_cause": "The Dockerfile COPY instruction references a path missing from the build context.",
        "expected_fix_keywords": ["Dockerfile", "COPY", "path", "build context"],
    },
    {
        "id": "S5",
        "name": "GitHub Actions workflow configuration error",
        "raw_log": (
            "Invalid workflow file: .github/workflows/ci.yml#L12\n"
            "The workflow is not valid. .github/workflows/ci.yml (Line: 12, Col: 5): "
            "Unexpected value 'run-tests'"
        ),
        "expected_failure_type": "workflow_configuration_error",
        "expected_root_cause": "The GitHub Actions workflow contains an unsupported or misplaced key.",
        "expected_fix_keywords": ["workflow", "YAML", "GitHub Actions", "unexpected value"],
    },
]
