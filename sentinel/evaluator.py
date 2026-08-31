"""Regression comparison, metrics, and evaluator-consistency checks."""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from typing import Any, Iterable

from .graders import grade_output
from .schema import MODELS, ValidatedInputs


def _round(value: float) -> float:
    return round(value, 6)


def _model_metrics(rows: Iterable[dict[str, Any]], model: str) -> dict[str, Any]:
    outcomes = [row[model] for row in rows]
    passed = sum(outcome["status"] == "pass" for outcome in outcomes)
    failed = sum(outcome["status"] == "fail" for outcome in outcomes)
    pending = sum(outcome["status"] == "needs_human_review" for outcome in outcomes)
    scored = passed + failed
    return {
        "failed": failed,
        "label": model,
        "needs_human_review": pending,
        "overall": _round(passed / scored) if scored else None,
        "passed": passed,
        "scored": scored,
        "total": len(outcomes),
    }


def _transition(row: dict[str, Any]) -> str:
    a = row["model_A"]["status"]
    b = row["model_B"]["status"]
    if "needs_human_review" in {a, b}:
        return "needs_human_review"
    if a == "pass" and b == "pass":
        return "both_pass"
    if a == "fail" and b == "fail":
        return "both_fail"
    if a == "pass" and b == "fail":
        return "regression"
    if a == "fail" and b == "pass":
        return "improvement"
    raise AssertionError(f"unexpected transition {a!r} -> {b!r}")


def _transition_metrics(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    case_ids: dict[str, list[str]] = {
        "both_fail": [],
        "both_pass": [],
        "improvement": [],
        "needs_human_review": [],
        "regression": [],
    }
    for row in rows:
        case_ids[_transition(row)].append(row["case_id"])
    for values in case_ids.values():
        values.sort()
    return {
        "counts": {key: len(case_ids[key]) for key in sorted(case_ids)},
        "case_ids": {key: case_ids[key] for key in sorted(case_ids)},
    }


def _exact_two_sided_sign_test(regressions: int, improvements: int) -> dict[str, Any]:
    discordant = regressions + improvements
    if discordant == 0:
        p_value = 1.0
    else:
        lower = min(regressions, improvements)
        tail = sum(math.comb(discordant, i) for i in range(lower + 1)) / (2**discordant)
        p_value = min(1.0, 2 * tail)
    return {
        "discordant_pairs": discordant,
        "improvements": improvements,
        "regressions": regressions,
        "two_sided_p_value": _round(p_value),
        "warning": (
            "Descriptive exact sign test only. Synthetic, hand-constructed cases are not a "
            "random sample and do not support production-population inference."
        ),
    }


def _gold_checks(
    rows: list[dict[str, Any]], gold: dict[str, dict[str, Any]]
) -> tuple[dict[str, Any], float | None]:
    status_counts = Counter(record["review_status"] for record in gold.values())
    all_human_reviewed = bool(gold) and set(status_counts) == {"HUMAN REVIEWED"}
    comparable = 0
    agreements = 0
    pending_judgments = 0
    disagreements: list[dict[str, Any]] = []

    rows_by_id = {row["case_id"]: row for row in rows}
    for case_id in sorted(gold):
        record = gold[case_id]
        for model in MODELS:
            expected = record["judgments"][model]
            measured = rows_by_id[case_id][model]
            if expected["outcome"] == "PENDING HUMAN REVIEW":
                pending_judgments += 1
                continue
            if measured["status"] == "needs_human_review":
                continue
            comparable += 1
            if measured["status"] == expected["outcome"]:
                agreements += 1
            else:
                disagreements.append(
                    {
                        "case_id": case_id,
                        "measured_status": measured["status"],
                        "model": model,
                        "reference_outcome": expected["outcome"],
                        "reference_rationale": expected["rationale"],
                    }
                )

    consistency_rate = _round(agreements / comparable) if comparable else None
    human_judge_agreement = consistency_rate if all_human_reviewed else None
    consistency_scope = (
        "This compares deterministic measurements with response-bound records marked HUMAN "
        "REVIEWED. It is recorded judge agreement, not independent verification of reviewer identity."
        if all_human_reviewed
        else "This compares deterministic measurements with AI-drafted provisional labels. It is "
        "an evaluator-audit signal, not human judge agreement or validation."
    )
    check = {
        "all_human_reviewed": all_human_reviewed,
        "human_reviewed_cases": status_counts.get("HUMAN REVIEWED", 0),
        "pending_human_review_cases": status_counts.get("PENDING HUMAN REVIEW", 0),
        "review_status_counts": dict(sorted(status_counts.items())),
        "deterministic_label_consistency": {
            "agreements": agreements,
            "comparable_judgments": comparable,
            "consistency_rate": consistency_rate,
            "disagreements": disagreements,
            "pending_judgments": pending_judgments,
            "scope_warning": consistency_scope,
        },
    }
    return check, human_judge_agreement


def _authoritative_gold_scoring(
    measured_rows: list[dict[str, Any]], gold: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    """Score human-reviewed gold only when the entire set is review-complete."""

    if not gold or any(record["review_status"] != "HUMAN REVIEWED" for record in gold.values()):
        return {
            "case_results": None,
            "delta": None,
            "dimensions": None,
            "failure_taxonomy": None,
            "model_a": None,
            "model_b": None,
            "status": "PENDING HUMAN REVIEW",
            "transitions": None,
            "warning": (
                "Gold-authoritative scoring is withheld until every response-bound gold record "
                "is marked HUMAN REVIEWED and contains no pending judgment."
            ),
        }

    measured_by_id = {row["case_id"]: row for row in measured_rows}
    gold_rows: list[dict[str, Any]] = []
    taxonomy: dict[str, Counter[str]] = {model: Counter() for model in MODELS}
    for case_id in sorted(gold):
        measured = measured_by_id[case_id]
        row: dict[str, Any] = {
            "case_id": case_id,
            "critical": measured["critical"],
            "dimension": measured["dimension"],
        }
        for model in MODELS:
            judgment = gold[case_id]["judgments"][model]
            status = judgment["outcome"]
            if status not in {"pass", "fail"}:
                raise AssertionError("review-complete gold retained a pending judgment")
            row[model] = {
                "failure_type": judgment["failure_type"],
                "score": 1 if status == "pass" else 0,
                "status": status,
            }
            if status == "fail":
                taxonomy[model][judgment["failure_type"]] += 1
        row["pair_outcome"] = _transition(row)
        gold_rows.append(row)

    model_a = _model_metrics(gold_rows, "model_A")
    model_b = _model_metrics(gold_rows, "model_B")
    dimension_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in gold_rows:
        dimension_rows[row["dimension"]].append(row)
    dimensions: dict[str, Any] = {}
    for dimension in sorted(dimension_rows):
        subset = dimension_rows[dimension]
        a = _model_metrics(subset, "model_A")
        b = _model_metrics(subset, "model_B")
        dimensions[dimension] = {
            "cases": len(subset),
            "delta": _round(b["overall"] - a["overall"]),
            "model_A": a,
            "model_B": b,
            "transitions": _transition_metrics(subset),
        }

    return {
        "case_results": gold_rows,
        "delta": _round(model_b["overall"] - model_a["overall"]),
        "dimensions": dimensions,
        "failure_taxonomy": {
            model: dict(sorted(taxonomy[model].items())) for model in MODELS
        },
        "model_a": model_a,
        "model_b": model_b,
        "status": "AVAILABLE",
        "transitions": _transition_metrics(gold_rows),
        "warning": (
            "These metrics reflect response-bound records marked HUMAN REVIEWED; the repository "
            "does not independently verify reviewer identity. They remain "
            "synthetic-suite results and do not determine the final ship decision."
        ),
    }


def evaluate_validated(
    inputs: ValidatedInputs,
    *,
    input_sha256: dict[str, str],
) -> dict[str, Any]:
    """Compute a stable summary from fully preflighted inputs."""

    rows: list[dict[str, Any]] = []
    failure_taxonomy: dict[str, Counter[str]] = {model: Counter() for model in MODELS}
    grader_failure_taxonomy: dict[str, Counter[str]] = {model: Counter() for model in MODELS}
    critical_failures: list[dict[str, str]] = []
    grader_counts: Counter[str] = Counter()

    for case_id in sorted(inputs.evals):
        case = inputs.evals[case_id]
        grader = case["grader"]
        grader_counts[grader["type"]] += 1
        row: dict[str, Any] = {
            "case_id": case_id,
            "critical": case["critical"],
            "dimension": case["dimension"],
            "grader": grader["type"],
            "success_criterion": case["success_criterion"],
        }
        for model in MODELS:
            response = inputs.responses[(case_id, model)]
            grade = grade_output(response["output"], grader)
            failure_type = case["failure_type"] if grade.status == "fail" else None
            row[model] = {
                "detail": grade.detail,
                "failure_type": failure_type,
                "grader_failure_code": grade.reason_code,
                "score": grade.score,
                "status": grade.status,
            }
            if grade.status == "fail":
                failure_taxonomy[model][case["failure_type"]] += 1
                if grade.reason_code is None:
                    raise AssertionError("failed deterministic grade has no reason code")
                grader_failure_taxonomy[model][grade.reason_code] += 1
                if case["critical"]:
                    critical_failures.append(
                        {
                            "case_id": case_id,
                            "detail": grade.detail,
                            "dimension": case["dimension"],
                            "failure_type": case["failure_type"],
                            "grader_failure_code": grade.reason_code,
                            "model": model,
                            "success_criterion": case["success_criterion"],
                        }
                    )
        row["pair_outcome"] = _transition(row)
        rows.append(row)

    model_a = _model_metrics(rows, "model_A")
    model_b = _model_metrics(rows, "model_B")
    delta = (
        _round(model_b["overall"] - model_a["overall"])
        if model_a["overall"] is not None and model_b["overall"] is not None
        else None
    )

    dimension_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        dimension_rows[row["dimension"]].append(row)
    dimensions: dict[str, Any] = {}
    for dimension in sorted(dimension_rows):
        subset = dimension_rows[dimension]
        a = _model_metrics(subset, "model_A")
        b = _model_metrics(subset, "model_B")
        dimensions[dimension] = {
            "cases": len(subset),
            "delta": (
                _round(b["overall"] - a["overall"])
                if a["overall"] is not None and b["overall"] is not None
                else None
            ),
            "model_A": a,
            "model_B": b,
            "transitions": _transition_metrics(subset),
        }

    transitions = _transition_metrics(rows)
    transition_counts = transitions["counts"]
    gold_review, judge_agreement = _gold_checks(rows, inputs.gold)
    authoritative_gold = _authoritative_gold_scoring(rows, inputs.gold)
    boundary_cases = [
        {
            "case_id": row["case_id"],
            "dimension": row["dimension"],
            "reason": row["model_A"]["detail"],
        }
        for row in rows
        if row["pair_outcome"] == "needs_human_review"
    ]

    synthetic_case_count = sum(case["synthetic"] for case in inputs.evals.values())
    summary: dict[str, Any] = {
        "authoritative_gold_scoring": authoritative_gold,
        "boundary_cases": boundary_cases,
        "cases": len(rows),
        "critical_failures": sorted(
            critical_failures,
            key=lambda item: (item["case_id"], item["model"]),
        ),
        "dataset": {
            "all_cases_synthetic": synthetic_case_count == len(rows),
            "automatically_scorable_cases": model_a["scored"],
            "automatic_coverage": _round(model_a["scored"] / len(rows)),
            "case_count": len(rows),
            "dimension_count": len(dimensions),
            "grader_counts": dict(sorted(grader_counts.items())),
            "human_review_required_cases": model_a["needs_human_review"],
            "synthetic_case_count": synthetic_case_count,
        },
        "delta": delta,
        "dimensions": dimensions,
        "failure_taxonomy": {
            model: dict(sorted(failure_taxonomy[model].items())) for model in MODELS
        },
        "final_decision": None,
        "gold_review": gold_review,
        "grader_failure_taxonomy": {
            model: dict(sorted(grader_failure_taxonomy[model].items())) for model in MODELS
        },
        "input_sha256": dict(sorted(input_sha256.items())),
        "judge_agreement": judge_agreement,
        "measurement_scope": (
            "Deterministic measurements of synthetic fixtures against AI-drafted expected "
            "conditions; no production-model inference."
        ),
        "model_a": model_a,
        "model_b": model_b,
        "paired_sign_test": _exact_two_sided_sign_test(
            transition_counts["regression"], transition_counts["improvement"]
        ),
        "schema_version": "1.0",
        "transitions": transitions,
        "validation": {
            "expected_gold_records": len(rows),
            "expected_response_pairs": len(rows) * len(MODELS),
            "status": "passed",
        },
        "case_results": rows,
    }
    return summary
