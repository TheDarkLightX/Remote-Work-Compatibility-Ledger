"""Path-level orchestration for a Sentinel evaluation run."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .evaluator import evaluate_validated
from .io import atomic_write_text, load_jsonl, stable_json
from .report import render_report
from .schema import validate_inputs


def run_evaluation(
    *,
    evals_path: Path,
    responses_path: Path,
    gold_path: Path,
    out_dir: Path,
) -> dict[str, Any]:
    """Validate all inputs, measure them, then replace deterministic outputs."""

    loaded_evals = load_jsonl(evals_path, "evals")
    loaded_responses = load_jsonl(responses_path, "responses")
    loaded_gold = load_jsonl(gold_path, "gold")

    validated = validate_inputs(
        loaded_evals.records,
        loaded_responses.records,
        loaded_gold.records,
    )
    summary = evaluate_validated(
        validated,
        input_sha256={
            "evals.jsonl": loaded_evals.sha256,
            "gold.jsonl": loaded_gold.sha256,
            "responses.jsonl": loaded_responses.sha256,
        },
    )
    summary_text = stable_json(summary)
    report_text = render_report(summary)

    # No output path is touched until parsing, schema checks, scoring, and
    # rendering have all completed successfully.
    atomic_write_text(out_dir / "summary.json", summary_text)
    atomic_write_text(out_dir / "report.md", report_text)
    return summary
