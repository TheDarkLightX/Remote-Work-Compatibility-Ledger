"""Generate the disclosed EVAL-001 synthetic fixture set.

This script creates the initial machine-authored inputs. It refuses to replace
existing files unless ``--force`` is supplied so a later human-reviewed gold
set cannot be overwritten accidentally.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sentinel.graders import grade_output
from sentinel.io import canonical_sha256


def exact(expected: str, **normalization: bool) -> dict[str, Any]:
    grader: dict[str, Any] = {"type": "exact_match", "expected": expected}
    if normalization:
        grader["normalization"] = normalization
    return grader


def substring(required: list[str], forbidden: list[str] | None = None) -> dict[str, Any]:
    return {
        "type": "substring",
        "required": required,
        "forbidden": forbidden or [],
        "case_sensitive": False,
    }


def membership(allowed: list[str]) -> dict[str, Any]:
    return {
        "type": "set_membership",
        "allowed": allowed,
        "case_sensitive": True,
        "strip": True,
    }


def regex(pattern: str) -> dict[str, Any]:
    return {
        "type": "regex",
        "pattern": pattern,
        "match_mode": "fullmatch",
        "case_sensitive": True,
    }


def valid_json(expected_type: str) -> dict[str, Any]:
    return {"type": "valid_json", "expected_type": expected_type}


def json_structure(
    required_keys: list[str],
    value_types: dict[str, str],
    required_values: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "type": "json_structure",
        "required_keys": required_keys,
        "forbidden_keys": [],
        "exact_keys": True,
        "value_types": value_types,
        "required_values": required_values or {},
    }


def numeric(expected: int | float, tolerance: float = 0) -> dict[str, Any]:
    return {
        "type": "numeric_tolerance",
        "expected": expected,
        "absolute_tolerance": tolerance,
        "relative_tolerance": 0,
    }


def case(
    case_id: str,
    dimension: str,
    prompt: str,
    success_criterion: str,
    grader: dict[str, Any],
    failure_type: str,
    model_a: str,
    model_b: str,
    *,
    critical: bool = False,
    gold_override: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "eval": {
            "case_id": case_id,
            "dimension": dimension,
            "prompt": prompt,
            "success_criterion": success_criterion,
            "synthetic": True,
            "grader": grader,
            "failure_type": failure_type,
            "critical": critical,
        },
        "outputs": {"model_A": model_a, "model_B": model_b},
        "gold_override": gold_override or {},
    }


def build_cases() -> list[dict[str, Any]]:
    cases = [
        case(
            "fg-001",
            "factuality_grounding",
            'Synthetic source [S1]: "The Helios probe launched in 1998." Return only the launch year.',
            "The output is exactly the source-supported year 1998 after trimming edge whitespace.",
            exact("1998", strip=True),
            "factual_mismatch",
            "1998",
            "1998",
        ),
        case(
            "fg-002",
            "factuality_grounding",
            'Synthetic source [S1]: "The North Annex opened in 2012." Return only the opening year.',
            "The output is exactly the source-supported year 2012 after trimming edge whitespace.",
            exact("2012", strip=True),
            "unsupported_factual_claim",
            "2012",
            "2013",
        ),
        case(
            "fg-003",
            "factuality_grounding",
            "Synthetic sources disagree: [S1] says the population is 12,000; [S2] says it is 14,000. Do not reconcile them. State the conflict in one sentence.",
            "The answer explicitly states the conflict and both reported values without claiming certainty.",
            substring(["conflict", "12,000", "14,000"], ["definitely"]),
            "source_conflict_ignored",
            "The population is 12,000.",
            "The sources conflict: S1 says 12,000 and S2 says 14,000.",
        ),
        case(
            "fg-004",
            "factuality_grounding",
            'Synthetic source [S1]: "Ticket R7 status: pending." Return only the status token.',
            "The trimmed output is the single allowed token pending.",
            membership(["pending"]),
            "factual_mismatch",
            "pending",
            "pending",
        ),
        case(
            "fg-005",
            "factuality_grounding",
            'Synthetic source [S1]: "The hard cap is 20 requests per minute." Respond exactly in this citation format: The limit is 20. [S1]',
            "The entire output matches the requested source-bound citation format.",
            regex(r"^The limit is 20\. \[S1\]$"),
            "citation_format_error",
            "The limit is 20. [S1]",
            "The limit is 20. [S1]",
        ),
        case(
            "fg-006",
            "factuality_grounding",
            'Synthetic source [S1]: "Arbor is the internal codename; no public product name is given." State only what the source supports.',
            "The answer identifies Arbor as internal and does not invent a public launch or product name.",
            substring(["Arbor", "internal"], ["publicly launched", "Project Oak"]),
            "unsupported_factual_claim",
            "The source identifies the internal codename as Arbor.",
            "The source identifies the internal codename as Arbor.",
        ),
        case(
            "if-001",
            "instruction_following",
            "Return exactly ACK with no punctuation or explanation.",
            "The complete output is exactly ACK.",
            exact("ACK"),
            "exact_format_violation",
            "ACK",
            "ACK.",
        ),
        case(
            "if-002",
            "instruction_following",
            "Return the identifier ABC-0420 using exactly three uppercase ASCII letters, a hyphen, and four digits.",
            "The complete output matches the requested uppercase identifier format.",
            regex(r"^[A-Z]{3}-[0-9]{4}$"),
            "regex_format_violation",
            "abc-0420",
            "ABC-0420",
        ),
        case(
            "if-003",
            "instruction_following",
            "Write one sentence containing alpha and beta. Do not mention gamma.",
            "The answer contains alpha and beta and omits gamma.",
            substring(["alpha", "beta"], ["gamma"]),
            "forbidden_content",
            "Alpha and beta are listed.",
            "Alpha and beta are listed.",
        ),
        case(
            "if-004",
            "instruction_following",
            "Return exactly an empty JSON array and nothing else.",
            "The complete output is exactly [].",
            exact("[]"),
            "exact_format_violation",
            "[]",
            "[]",
        ),
        case(
            "if-005",
            "instruction_following",
            "Return only blue or green. The rule for this case says choose green.",
            "The trimmed output is the allowed and instructed token green.",
            membership(["green"]),
            "set_membership_violation",
            "green",
            "green",
        ),
        case(
            "if-006",
            "instruction_following",
            "Return exactly three lowercase comma-delimited words with no spaces. Any three lowercase words are allowed.",
            "The complete output is three lowercase comma-delimited words with no spaces.",
            regex(r"^[a-z]+,[a-z]+,[a-z]+$"),
            "regex_format_violation",
            "oak,pine,birch",
            "oak,pine,birch",
        ),
        case(
            "so-001",
            "structured_output",
            "Return any valid JSON object that records ok=true. No prose.",
            "The object has exactly ok:boolean with ok=true.",
            json_structure(["ok"], {"ok": "boolean"}, {"ok": True}),
            "invalid_json",
            '{"ok":true}',
            "{'ok': true}",
            critical=True,
        ),
        case(
            "so-002",
            "structured_output",
            "Return one JSON object with exactly two keys: id must be a string and count must be an integer.",
            "The object has exactly id:string and count:integer.",
            json_structure(["id", "count"], {"id": "string", "count": "integer"}),
            "wrong_json_type",
            '{"id":"x","count":2}',
            '{"id":"x","count":"2"}',
            critical=True,
        ),
        case(
            "so-003",
            "structured_output",
            "Return any syntactically valid JSON value. No prose.",
            "The complete output parses as standards-compliant JSON of any type.",
            valid_json("any"),
            "invalid_json",
            "[1,2,3]",
            '{"values":[1,2,3]}',
        ),
        case(
            "so-004",
            "structured_output",
            "Return one JSON object with exactly name:string and tags:array.",
            "The object has exactly name:string and tags:array.",
            json_structure(["name", "tags"], {"name": "string", "tags": "array"}),
            "json_contract_violation",
            '{"name":"sample","tags":["red","blue"]}',
            '{"name":"sample","tags":["red","blue"]}',
        ),
        case(
            "so-005",
            "structured_output",
            'Return exactly this minified JSON and nothing else: {"status":"ok"}',
            'The complete output is exactly {"status":"ok"}.',
            exact('{"status":"ok"}'),
            "exact_format_violation",
            '{"status":"ok"}',
            '{"status":"ok"}',
        ),
        case(
            "so-006",
            "structured_output",
            "Return one JSON object with exactly active:boolean and retries:integer.",
            "The object has exactly active:boolean and retries:integer; booleans are not integers.",
            json_structure(["active", "retries"], {"active": "boolean", "retries": "integer"}),
            "json_contract_violation",
            '{"active":false,"retries":0}',
            '{"active":false,"retries":0}',
        ),
        case(
            "cu-001",
            "calibrated_uncertainty",
            "Synthetic evidence reports an association between treatment use and improvement, with no randomized assignment. State whether causation is established.",
            "The answer states there is insufficient evidence and avoids definitely/proves.",
            substring(["insufficient evidence"], ["definitely", "proves"]),
            "overconfidence",
            "The treatment definitely caused the improvement.",
            "There is insufficient evidence to infer that the treatment caused the improvement.",
        ),
        case(
            "cu-002",
            "calibrated_uncertainty",
            "A coin was tossed once and landed heads. Return only whether its bias can be determined: fair, biased, or cannot determine.",
            "The trimmed output is cannot determine.",
            membership(["cannot determine"]),
            "uncertainty_not_expressed",
            "fair",
            "cannot determine",
        ),
        case(
            "cu-003",
            "calibrated_uncertainty",
            "The sample has three observations. Describe the result using both words uncertain and estimate.",
            "The answer contains both uncertain and estimate.",
            substring(["uncertain", "estimate"]),
            "uncertainty_not_expressed",
            "This is an uncertain estimate based on three observations.",
            "This is an uncertain estimate based on three observations.",
        ),
        case(
            "cu-004",
            "calibrated_uncertainty",
            "A synthetic calibration specification assigns probability 0.60. Return only the numeric probability.",
            "The output is numeric and within 0.001 absolute error of 0.60.",
            numeric(0.60, 0.001),
            "numeric_tolerance_failure",
            "0.60",
            "0.60",
        ),
        case(
            "cu-005",
            "calibrated_uncertainty",
            "Return the stated uncertainty interval exactly as [0.30,0.50].",
            "The entire output is exactly the specified bracketed interval.",
            regex(r"^\[0\.30,0\.50\]$"),
            "regex_format_violation",
            "[0.30,0.50]",
            "[0.30,0.50]",
        ),
        case(
            "cu-006",
            "calibrated_uncertainty",
            'An observational report says users who opted into a feature retained more; it has no randomization or confounder controls. State whether the feature caused retention. A lexical checker requires the phrase "insufficient evidence".',
            "The lexical grader requires insufficient evidence; semantic stance still needs audit.",
            substring(["insufficient evidence"]),
            "semantic_negation_keyword_gaming",
            "There is insufficient evidence to conclude the feature caused higher retention.",
            "It is false that there is insufficient evidence; the feature definitely caused higher retention.",
            gold_override={
                "model_B": {
                    "outcome": "fail",
                    "failure_type": "semantic_negation_keyword_gaming",
                    "rationale": (
                        "AI-drafted provisional label: the required phrase is negated and followed by "
                        "an unsupported causal claim; the lexical grader is misleading here. "
                        "PENDING HUMAN REVIEW."
                    ),
                }
            },
        ),
        case(
            "cu-007",
            "calibrated_uncertainty",
            'Synthetic policy excerpt: "Notify compliance before a material user-interface change." The policy does not define material. Scenario: a status label changes from gray to blue with no wording or workflow change. Decide whether notification is required and justify briefly.',
            "No deterministic label is justified until a human resolves the undefined term material.",
            {
                "type": "human_review_required",
                "reason": "Undefined policy term makes deterministic pass/fail unsupported.",
            },
            "ambiguous_policy_boundary",
            "No notification is required because only the color changed.",
            "The excerpt is insufficient to decide whether a color-only change is material; compliance interpretation is required.",
        ),
        case(
            "rc-001",
            "reasoning_consistency",
            "Compute 7 × 6. Return only the number.",
            "The numeric output equals 42 exactly.",
            numeric(42),
            "arithmetic_error",
            "42",
            "41",
        ),
        case(
            "rc-002",
            "reasoning_consistency",
            "Compute the arithmetic mean of 2 and 3. Return only the number.",
            "The numeric output is within 0.001 absolute error of 2.5.",
            numeric(2.5, 0.001),
            "arithmetic_error",
            "2.4",
            "2.5",
        ),
        case(
            "rc-003",
            "reasoning_consistency",
            "Every Nerp is blue. Object Q is a Nerp. Is Q blue? Return only yes or no.",
            "The trimmed, case-insensitive output is yes.",
            exact("yes", strip=True, casefold=True),
            "logical_inconsistency",
            "yes",
            "yes",
        ),
        case(
            "rc-004",
            "reasoning_consistency",
            "A is before B, and B is before C. Return only A_before_C or C_before_A.",
            "The trimmed output is the allowed conclusion A_before_C.",
            membership(["A_before_C"]),
            "logical_inconsistency",
            "A_before_C",
            "A_before_C",
        ),
        case(
            "rc-005",
            "reasoning_consistency",
            "Continue 2, 4, 8 with the next value. Return only the integer.",
            "The complete output is exactly 16.",
            exact("16"),
            "sequence_error",
            "16",
            "16",
        ),
        case(
            "rc-006",
            "reasoning_consistency",
            "Synthetic policy says accept if and only if score is at least 80. A record has score 79 and accepted=true. In one sentence, identify the inconsistency.",
            "The answer contains contradiction and the boundary value 79.",
            substring(["contradiction", "79"]),
            "logical_inconsistency",
            "There is a contradiction: a score of 79 should not be accepted.",
            "There is a contradiction: a score of 79 should not be accepted.",
        ),
        case(
            "ta-001",
            "tool_api_arguments",
            'Create the exact minified tool call for a 3-day Boston weather lookup: {"tool":"weather","location":"Boston, MA","days":3}',
            "The complete output exactly matches the specified minified tool call.",
            exact('{"tool":"weather","location":"Boston, MA","days":3}'),
            "wrong_argument_value",
            '{"tool":"weather","location":"Boston, MA","days":3}',
            '{"tool":"weather","location":"Boston, MA","days":5}',
        ),
        case(
            "ta-002",
            "tool_api_arguments",
            "Return a JSON search call with exactly tool:string, query:string, and limit:integer. Use tool=search, query=release notes, limit=5.",
            "The object has exactly the required keys/types and the specified argument values.",
            json_structure(
                ["tool", "query", "limit"],
                {"tool": "string", "query": "string", "limit": "integer"},
                {"tool": "search", "query": "release notes", "limit": 5},
            ),
            "missing_required_argument",
            '{"tool":"search","limit":5}',
            '{"tool":"search","query":"release notes","limit":5}',
        ),
        case(
            "ta-003",
            "tool_api_arguments",
            "The synthetic API sets retry_after to exactly 30 seconds. Return only the numeric argument.",
            "The numeric output equals 30 exactly.",
            numeric(30),
            "wrong_argument_value",
            "30",
            "30",
        ),
        case(
            "ta-004",
            "tool_api_arguments",
            "The operation permits only read_only access. Return the one allowed enum token.",
            "The trimmed output is the one allowed enum token read_only.",
            membership(["read_only"]),
            "invalid_enum_value",
            "read_only",
            "read_only",
        ),
        case(
            "ta-005",
            "tool_api_arguments",
            "Return the scheduled date as ISO YYYY-MM-DD. The date is 2026-09-01.",
            "The complete output matches the specified ISO date.",
            regex(r"^2026-09-01$"),
            "date_format_error",
            "2026-09-01",
            "2026-09-01",
        ),
        case(
            "ta-006",
            "tool_api_arguments",
            "Write the synthetic deployment call for target staging with dry_run=true. Do not use force=true.",
            "The answer contains target=staging and dry_run=true and omits force=true.",
            substring(["target=staging", "dry_run=true"], ["force=true"]),
            "unsafe_tool_argument",
            "deploy(target=staging,dry_run=true)",
            "deploy(target=staging,dry_run=true)",
        ),
    ]
    return cases


def build_records() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    cases = build_cases()
    evals: list[dict[str, Any]] = []
    responses: list[dict[str, Any]] = []
    gold: list[dict[str, Any]] = []

    for item in cases:
        evaluation = item["eval"]
        case_id = evaluation["case_id"]
        fingerprint = canonical_sha256(evaluation)
        evals.append(evaluation)
        judgments: dict[str, dict[str, Any]] = {}
        for model in ("model_A", "model_B"):
            output = item["outputs"][model]
            response = {
                "case_id": case_id,
                "response_id": f"{case_id}::{model}",
                "model": model,
                "eval_sha256": fingerprint,
                "output": output,
                "synthetic": True,
            }
            responses.append(response)
            grade = grade_output(output, evaluation["grader"])
            if grade.status == "needs_human_review":
                judgment = {
                    "outcome": "PENDING HUMAN REVIEW",
                    "failure_type": None,
                    "rationale": "No automated label is asserted. PENDING HUMAN REVIEW.",
                    "response_sha256": canonical_sha256(response),
                }
            else:
                judgment = {
                    "outcome": grade.status,
                    "failure_type": evaluation["failure_type"] if grade.status == "fail" else None,
                    "rationale": (
                        f"AI-drafted provisional label: {grade.detail}. PENDING HUMAN REVIEW."
                    ),
                    "response_sha256": canonical_sha256(response),
                }
            judgment.update(item["gold_override"].get(model, {}))
            judgments[model] = judgment
        gold.append(
            {
                "case_id": case_id,
                "eval_sha256": fingerprint,
                "review_status": "PENDING HUMAN REVIEW",
                "drafted_by": "OpenAI Codex (AI)",
                "reviewed_by": None,
                "reviewed_at": None,
                "judgments": judgments,
            }
        )

    # Guard the intended experimental shape against accidental generator edits.
    dimensions = {record["dimension"] for record in evals}
    grader_types = {record["grader"]["type"] for record in evals}
    grades = {
        model: [grade_output(item["outputs"][model], item["eval"]["grader"]) for item in cases]
        for model in ("model_A", "model_B")
    }
    assert len(evals) == 37
    assert len(dimensions) == 6
    assert len(grader_types) == 8
    assert all(sum(g.status == "pass" for g in grades[model]) == 30 for model in grades)
    assert all(sum(g.status == "fail" for g in grades[model]) == 6 for model in grades)
    assert all(sum(g.status == "needs_human_review" for g in grades[model]) == 1 for model in grades)
    return evals, responses, gold


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    content = "".join(
        json.dumps(record, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        + "\n"
        for record in records
    )
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("submissions/EVAL-001/dana-v1"),
        help="submission directory",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace existing machine-authored files (can destroy later human edits)",
    )
    args = parser.parse_args()
    targets = [args.out / name for name in ("evals.jsonl", "responses.jsonl", "gold.jsonl")]
    existing = [path for path in targets if path.exists()]
    if existing and not args.force:
        parser.error(
            "refusing to replace existing files without --force: "
            + ", ".join(str(path) for path in existing)
        )

    evals, responses, gold = build_records()
    args.out.mkdir(parents=True, exist_ok=True)
    for path, records in zip(targets, (evals, responses, gold)):
        write_jsonl(path, records)
        print(f"WROTE: {path} ({len(records)} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
