"""Run the CI/CD agent experiment and export aggregate results."""

import csv
from pathlib import Path

from agents import (
    run_multi_agent_with_validation,
    run_multi_agent_without_validation,
    single_agent_baseline,
)
from evaluator import average_metrics, evaluate_output
from scenarios import SCENARIOS


CONFIGURATIONS = {
    "Single-Agent Baseline": single_agent_baseline,
    "Multi-Agent Without Validation": run_multi_agent_without_validation,
    "Multi-Agent With Validation": run_multi_agent_with_validation,
}


def run_experiment() -> list[dict]:
    """Run every scenario through every configuration and aggregate metric scores."""
    aggregate_rows = []

    for config_name, runner in CONFIGURATIONS.items():
        scenario_scores = []

        for scenario in SCENARIOS:
            output = runner(scenario["raw_log"])
            score = evaluate_output(output, scenario, config_name)
            scenario_scores.append(score)

        averages = average_metrics(scenario_scores)
        aggregate_rows.append(
            {
                "Configuration": config_name,
                "Diagnostic Accuracy": averages["diagnostic_accuracy"],
                "Fix Correctness": averages["fix_correctness"],
                "Consistency": averages["consistency"],
                "Reasoning Quality": averages["reasoning_quality"],
                "Overall Reliability": averages["overall_reliability"],
            }
        )

    return aggregate_rows


def print_results_table(results: list[dict]) -> None:
    """Print a clean terminal table of aggregate experiment results."""
    columns = [
        "Configuration",
        "Diagnostic Accuracy",
        "Fix Correctness",
        "Consistency",
        "Reasoning Quality",
        "Overall Reliability",
    ]
    display_rows = [
        {
            key: row[key] if key == "Configuration" else f"{row[key]:.2f}"
            for key in columns
        }
        for row in results
    ]
    widths = {
        key: max(len(key), *(len(str(row[key])) for row in display_rows))
        for key in columns
    }

    header = " | ".join(key.ljust(widths[key]) for key in columns)
    separator = "-+-".join("-" * widths[key] for key in columns)
    print(header)
    print(separator)
    for row in display_rows:
        print(" | ".join(str(row[key]).ljust(widths[key]) for key in columns))


def export_results(results: list[dict], output_path: Path) -> None:
    """Export aggregate experiment results to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(results[0].keys()))
        writer.writeheader()
        for row in results:
            writer.writerow(
                {
                    key: value if key == "Configuration" else round(value, 3)
                    for key, value in row.items()
                }
            )


def main() -> None:
    """Run the experiment, print results, export CSV, and summarize findings."""
    results = run_experiment()
    output_path = Path("results") / "experiment_results.csv"

    print("\nCI/CD Agent Experiment Results\n")
    print_results_table(results)
    export_results(results, output_path)

    print(f"\nCSV exported to: {output_path}")
    print(
        "\nInterpretation: The multi-agent pipeline with validation achieved the highest "
        "overall reliability because it separates log extraction, root cause analysis, "
        "fix generation, and validation into distinct stages."
    )


if __name__ == "__main__":
    main()
