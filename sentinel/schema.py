"""Fail-closed record validation for the Sentinel JSONL contracts."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any, Iterable

from .errors import (
    AlignmentError,
    CoverageError,
    DuplicateIDError,
    GraderConfigurationError,
    SchemaValidationError,
)
from .io import canonical_sha256

MODELS = ("model_A", "model_B")
OUTCOMES = {"pass", "fail", "PENDING HUMAN REVIEW"}
REVIEW_STATUSES = {"PENDING HUMAN REVIEW", "HUMAN REVIEWED"}
JSON_TYPES = {"object", "array", "string", "number", "integer", "boolean", "null"}
VALID_JSON_EXPECTED_TYPES = JSON_TYPES | {"any"}
CASE_ID = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
NAME = re.compile(r"^[a-z][a-z0-9_]{1,63}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class ValidatedInputs:
    evals: dict[str, dict[str, Any]]
    responses: dict[tuple[str, str], dict[str, Any]]
    gold: dict[str, dict[str, Any]]


def _location(kind: str, line_number: int | None = None) -> str:
    return f"{kind} line {line_number}" if line_number is not None else kind


def _require_exact_keys(
    value: dict[str, Any],
    *,
    required: set[str],
    optional: set[str] = frozenset(),
    context: str,
    error_type: type[SchemaValidationError] = SchemaValidationError,
) -> None:
    actual = set(value)
    missing = sorted(required - actual)
    extra = sorted(actual - required - optional)
    if missing or extra:
        parts: list[str] = []
        if missing:
            parts.append(f"missing keys: {', '.join(missing)}")
        if extra:
            parts.append(f"unknown keys: {', '.join(extra)}")
        raise error_type(f"{context}: {'; '.join(parts)}")


def _nonempty_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SchemaValidationError(f"{context} must be a non-empty string")
    return value


def _string_list(value: Any, context: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        qualifier = "a non-empty list" if not allow_empty else "a list"
        raise GraderConfigurationError(f"{context} must be {qualifier} of strings")
    if not all(isinstance(item, str) and item for item in value):
        raise GraderConfigurationError(f"{context} must contain only non-empty strings")
    if len(value) != len(set(value)):
        raise GraderConfigurationError(f"{context} contains duplicate values")
    return value


def _finite_number(value: Any, context: str) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise GraderConfigurationError(f"{context} must be a finite number")
    if isinstance(value, float) and not math.isfinite(value):
        raise GraderConfigurationError(f"{context} must be a finite number")
    return value


def _matches_declared_json_type(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "string":
        return isinstance(value, str)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    raise AssertionError(f"unknown validated JSON type {expected!r}")


def _validate_normalization(value: Any, context: str) -> None:
    if not isinstance(value, dict):
        raise GraderConfigurationError(f"{context} must be an object")
    _require_exact_keys(
        value,
        required=set(),
        optional={"strip", "casefold", "collapse_whitespace"},
        context=context,
        error_type=GraderConfigurationError,
    )
    for key, setting in value.items():
        if not isinstance(setting, bool):
            raise GraderConfigurationError(f"{context}.{key} must be boolean")


def validate_grader(grader: Any, context: str) -> None:
    if not isinstance(grader, dict):
        raise GraderConfigurationError(f"{context} must be an object")
    grader_type = grader.get("type")
    if not isinstance(grader_type, str):
        raise GraderConfigurationError(f"{context}.type must be a string")

    if grader_type == "exact_match":
        _require_exact_keys(
            grader,
            required={"type", "expected"},
            optional={"normalization"},
            context=context,
            error_type=GraderConfigurationError,
        )
        if not isinstance(grader["expected"], str):
            raise GraderConfigurationError(f"{context}.expected must be a string")
        if "normalization" in grader:
            _validate_normalization(grader["normalization"], f"{context}.normalization")
        return

    if grader_type == "substring":
        _require_exact_keys(
            grader,
            required={"type", "required", "forbidden", "case_sensitive"},
            context=context,
            error_type=GraderConfigurationError,
        )
        required = _string_list(grader["required"], f"{context}.required")
        forbidden = _string_list(grader["forbidden"], f"{context}.forbidden")
        if not required and not forbidden:
            raise GraderConfigurationError(
                f"{context} must declare at least one required or forbidden substring"
            )
        if not isinstance(grader["case_sensitive"], bool):
            raise GraderConfigurationError(f"{context}.case_sensitive must be boolean")
        comparable_required = required if grader["case_sensitive"] else [x.casefold() for x in required]
        comparable_forbidden = forbidden if grader["case_sensitive"] else [x.casefold() for x in forbidden]
        overlap = sorted(set(comparable_required) & set(comparable_forbidden))
        if overlap:
            raise GraderConfigurationError(
                f"{context} requires and forbids the same substring(s): {', '.join(overlap)}"
            )
        return

    if grader_type == "valid_json":
        _require_exact_keys(
            grader,
            required={"type", "expected_type"},
            context=context,
            error_type=GraderConfigurationError,
        )
        if grader["expected_type"] not in VALID_JSON_EXPECTED_TYPES:
            raise GraderConfigurationError(
                f"{context}.expected_type must be one of "
                f"{', '.join(sorted(VALID_JSON_EXPECTED_TYPES))}"
            )
        return

    if grader_type == "json_structure":
        _require_exact_keys(
            grader,
            required={
                "type",
                "required_keys",
                "forbidden_keys",
                "exact_keys",
                "value_types",
                "required_values",
            },
            context=context,
            error_type=GraderConfigurationError,
        )
        required = _string_list(grader["required_keys"], f"{context}.required_keys")
        forbidden = _string_list(grader["forbidden_keys"], f"{context}.forbidden_keys")
        overlap = sorted(set(required) & set(forbidden))
        if overlap:
            raise GraderConfigurationError(
                f"{context} requires and forbids the same key(s): {', '.join(overlap)}"
            )
        if not isinstance(grader["exact_keys"], bool):
            raise GraderConfigurationError(f"{context}.exact_keys must be boolean")
        value_types = grader["value_types"]
        if not isinstance(value_types, dict):
            raise GraderConfigurationError(f"{context}.value_types must be an object")
        for key, expected_type in value_types.items():
            if not isinstance(key, str) or not key:
                raise GraderConfigurationError(f"{context}.value_types keys must be strings")
            if key not in required:
                raise GraderConfigurationError(
                    f"{context}.value_types key {key!r} must also be required"
                )
            if expected_type not in JSON_TYPES:
                raise GraderConfigurationError(
                    f"{context}.value_types[{key!r}] has unknown JSON type {expected_type!r}"
                )
        required_values = grader["required_values"]
        if not isinstance(required_values, dict):
            raise GraderConfigurationError(f"{context}.required_values must be an object")
        for key in required_values:
            if not isinstance(key, str) or not key:
                raise GraderConfigurationError(f"{context}.required_values keys must be strings")
            if key not in required:
                raise GraderConfigurationError(
                    f"{context}.required_values key {key!r} must also be required"
                )
            if key in value_types and not _matches_declared_json_type(
                required_values[key], value_types[key]
            ):
                raise GraderConfigurationError(
                    f"{context}.required_values[{key!r}] contradicts declared type "
                    f"{value_types[key]!r}"
                )
        if not required and not forbidden:
            raise GraderConfigurationError(f"{context} must constrain at least one key")
        return

    if grader_type == "numeric_tolerance":
        _require_exact_keys(
            grader,
            required={"type", "expected", "absolute_tolerance", "relative_tolerance"},
            context=context,
            error_type=GraderConfigurationError,
        )
        _finite_number(grader["expected"], f"{context}.expected")
        absolute = _finite_number(grader["absolute_tolerance"], f"{context}.absolute_tolerance")
        relative = _finite_number(grader["relative_tolerance"], f"{context}.relative_tolerance")
        if absolute < 0 or relative < 0:
            raise GraderConfigurationError(f"{context} tolerances must be non-negative")
        return

    if grader_type == "set_membership":
        _require_exact_keys(
            grader,
            required={"type", "allowed", "case_sensitive", "strip"},
            context=context,
            error_type=GraderConfigurationError,
        )
        allowed = _string_list(grader["allowed"], f"{context}.allowed", allow_empty=False)
        if not isinstance(grader["case_sensitive"], bool) or not isinstance(grader["strip"], bool):
            raise GraderConfigurationError(
                f"{context}.case_sensitive and {context}.strip must be boolean"
            )
        comparable = [item.strip() for item in allowed] if grader["strip"] else list(allowed)
        if not grader["case_sensitive"]:
            comparable = [item.casefold() for item in comparable]
        if len(comparable) != len(set(comparable)):
            raise GraderConfigurationError(
                f"{context}.allowed contains duplicates after configured normalization"
            )
        return

    if grader_type == "regex":
        _require_exact_keys(
            grader,
            required={"type", "pattern", "match_mode", "case_sensitive"},
            context=context,
            error_type=GraderConfigurationError,
        )
        pattern = grader["pattern"]
        if not isinstance(pattern, str) or not pattern or len(pattern) > 500:
            raise GraderConfigurationError(
                f"{context}.pattern must be a non-empty string of at most 500 characters"
            )
        if grader["match_mode"] not in {"fullmatch", "search"}:
            raise GraderConfigurationError(
                f"{context}.match_mode must be 'fullmatch' or 'search'"
            )
        if not isinstance(grader["case_sensitive"], bool):
            raise GraderConfigurationError(f"{context}.case_sensitive must be boolean")
        try:
            re.compile(pattern)
        except re.error as exc:
            raise GraderConfigurationError(f"{context}.pattern is invalid: {exc}") from exc
        return

    if grader_type == "human_review_required":
        _require_exact_keys(
            grader,
            required={"type", "reason"},
            context=context,
            error_type=GraderConfigurationError,
        )
        if not isinstance(grader["reason"], str) or not grader["reason"].strip():
            raise GraderConfigurationError(f"{context}.reason must be a non-empty string")
        return

    raise GraderConfigurationError(f"{context}.type has unknown grader {grader_type!r}")


def validate_evals(records: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    first_lines: dict[str, int] = {}
    required = {
        "case_id",
        "dimension",
        "prompt",
        "success_criterion",
        "synthetic",
        "grader",
        "failure_type",
        "critical",
    }
    for line_number, record in enumerate(records, start=1):
        context = _location("evals", line_number)
        _require_exact_keys(record, required=required, context=context)
        case_id = _nonempty_string(record["case_id"], f"{context}.case_id")
        if not CASE_ID.fullmatch(case_id):
            raise SchemaValidationError(f"{context}.case_id has invalid format: {case_id!r}")
        if case_id in result:
            raise DuplicateIDError(
                f"{context}: duplicate case_id {case_id!r}; first seen at evals line {first_lines[case_id]}"
            )
        dimension = _nonempty_string(record["dimension"], f"{context}.dimension")
        if not NAME.fullmatch(dimension):
            raise SchemaValidationError(f"{context}.dimension has invalid format: {dimension!r}")
        _nonempty_string(record["prompt"], f"{context}.prompt")
        _nonempty_string(record["success_criterion"], f"{context}.success_criterion")
        failure_type = _nonempty_string(record["failure_type"], f"{context}.failure_type")
        if not NAME.fullmatch(failure_type):
            raise SchemaValidationError(
                f"{context}.failure_type has invalid format: {failure_type!r}"
            )
        if not isinstance(record["synthetic"], bool):
            raise SchemaValidationError(f"{context}.synthetic must be boolean")
        if not isinstance(record["critical"], bool):
            raise SchemaValidationError(f"{context}.critical must be boolean")
        validate_grader(record["grader"], f"{context}.grader")
        result[case_id] = record
        first_lines[case_id] = line_number
    return result


def validate_responses(
    records: Iterable[dict[str, Any]], evals: dict[str, dict[str, Any]]
) -> dict[tuple[str, str], dict[str, Any]]:
    required = {"case_id", "response_id", "model", "eval_sha256", "output", "synthetic"}
    result: dict[tuple[str, str], dict[str, Any]] = {}
    first_lines: dict[tuple[str, str], int] = {}
    unknown_cases: list[str] = []

    for line_number, record in enumerate(records, start=1):
        context = _location("responses", line_number)
        _require_exact_keys(record, required=required, context=context)
        case_id = _nonempty_string(record["case_id"], f"{context}.case_id")
        model = record["model"]
        if model not in MODELS:
            raise SchemaValidationError(
                f"{context}.model must be exactly model_A or model_B; got {model!r}"
            )
        key = (case_id, model)
        if key in result:
            first = first_lines[key]
            raise DuplicateIDError(
                f"{context}: duplicate response pair {case_id!r}/{model}; first seen at responses line {first}"
            )
        expected_response_id = f"{case_id}::{model}"
        if record["response_id"] != expected_response_id:
            raise AlignmentError(
                f"{context}.response_id {record['response_id']!r} does not match "
                f"case/model binding {expected_response_id!r}"
            )
        if not isinstance(record["eval_sha256"], str) or not SHA256.fullmatch(record["eval_sha256"]):
            raise SchemaValidationError(f"{context}.eval_sha256 must be a lowercase SHA-256")
        if not isinstance(record["output"], str):
            raise SchemaValidationError(f"{context}.output must be a string")
        if not isinstance(record["synthetic"], bool):
            raise SchemaValidationError(f"{context}.synthetic must be boolean")
        if case_id not in evals:
            unknown_cases.append(case_id)
        else:
            expected_sha = canonical_sha256(evals[case_id])
            if record["eval_sha256"] != expected_sha:
                raise AlignmentError(
                    f"{context}: fingerprint mismatch for {case_id!r}; response may be swapped or stale"
                )
            if record["synthetic"] != evals[case_id]["synthetic"]:
                raise AlignmentError(
                    f"{context}: synthetic flag disagrees with eval {case_id!r}"
                )
        result[key] = record
        first_lines[key] = line_number

    expected_pairs = {(case_id, model) for case_id in evals for model in MODELS}
    actual_pairs = set(result)
    missing = sorted(expected_pairs - actual_pairs)
    unexpected = sorted(actual_pairs - expected_pairs)
    if missing or unexpected or unknown_cases:
        parts: list[str] = []
        if missing:
            parts.append("missing response pairs: " + _format_pairs(missing))
        if unexpected:
            parts.append("unexpected response pairs: " + _format_pairs(unexpected))
        raise CoverageError("responses do not exactly cover eval/model pairs; " + "; ".join(parts))
    return result


def _validate_judgment(value: Any, context: str) -> None:
    if not isinstance(value, dict):
        raise SchemaValidationError(f"{context} must be an object")
    _require_exact_keys(
        value,
        required={"outcome", "failure_type", "rationale", "response_sha256"},
        context=context,
    )
    outcome = value["outcome"]
    if outcome not in OUTCOMES:
        raise SchemaValidationError(
            f"{context}.outcome must be pass, fail, or PENDING HUMAN REVIEW"
        )
    failure_type = value["failure_type"]
    if failure_type is not None and (
        not isinstance(failure_type, str) or not NAME.fullmatch(failure_type)
    ):
        raise SchemaValidationError(f"{context}.failure_type must be null or a category name")
    if outcome == "pass" and failure_type is not None:
        raise SchemaValidationError(f"{context}: pass outcome must have null failure_type")
    if outcome == "fail" and failure_type is None:
        raise SchemaValidationError(f"{context}: fail outcome must name a failure_type")
    if not isinstance(value["response_sha256"], str) or not SHA256.fullmatch(
        value["response_sha256"]
    ):
        raise SchemaValidationError(f"{context}.response_sha256 must be a lowercase SHA-256")
    _nonempty_string(value["rationale"], f"{context}.rationale")


def validate_gold(
    records: Iterable[dict[str, Any]],
    evals: dict[str, dict[str, Any]],
    responses: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    required = {
        "case_id",
        "eval_sha256",
        "review_status",
        "drafted_by",
        "reviewed_by",
        "reviewed_at",
        "judgments",
    }
    result: dict[str, dict[str, Any]] = {}
    first_lines: dict[str, int] = {}

    for line_number, record in enumerate(records, start=1):
        context = _location("gold", line_number)
        _require_exact_keys(record, required=required, context=context)
        case_id = _nonempty_string(record["case_id"], f"{context}.case_id")
        if case_id in result:
            raise DuplicateIDError(
                f"{context}: duplicate case_id {case_id!r}; first seen at gold line {first_lines[case_id]}"
            )
        if case_id not in evals:
            result[case_id] = record
            first_lines[case_id] = line_number
            continue
        if not isinstance(record["eval_sha256"], str) or not SHA256.fullmatch(record["eval_sha256"]):
            raise SchemaValidationError(f"{context}.eval_sha256 must be a lowercase SHA-256")
        if record["eval_sha256"] != canonical_sha256(evals[case_id]):
            raise AlignmentError(
                f"{context}: fingerprint mismatch for {case_id!r}; gold may be swapped or stale"
            )
        if record["review_status"] not in REVIEW_STATUSES:
            raise SchemaValidationError(
                f"{context}.review_status must be PENDING HUMAN REVIEW or HUMAN REVIEWED"
            )
        _nonempty_string(record["drafted_by"], f"{context}.drafted_by")
        if record["review_status"] == "PENDING HUMAN REVIEW":
            if record["reviewed_by"] is not None or record["reviewed_at"] is not None:
                raise SchemaValidationError(
                    f"{context}: pending record must keep reviewed_by and reviewed_at null"
                )
        else:
            _nonempty_string(record["reviewed_by"], f"{context}.reviewed_by")
            _nonempty_string(record["reviewed_at"], f"{context}.reviewed_at")
        judgments = record["judgments"]
        if not isinstance(judgments, dict):
            raise SchemaValidationError(f"{context}.judgments must be an object")
        _require_exact_keys(judgments, required=set(MODELS), context=f"{context}.judgments")
        for model in MODELS:
            _validate_judgment(judgments[model], f"{context}.judgments.{model}")
            expected_response_sha = canonical_sha256(responses[(case_id, model)])
            if judgments[model]["response_sha256"] != expected_response_sha:
                raise AlignmentError(
                    f"{context}.judgments.{model}: response fingerprint mismatch for "
                    f"{case_id!r}; gold may bind a stale or swapped output"
                )
        if record["review_status"] == "HUMAN REVIEWED" and any(
            judgments[model]["outcome"] == "PENDING HUMAN REVIEW" for model in MODELS
        ):
            raise SchemaValidationError(
                f"{context}: HUMAN REVIEWED record cannot retain pending judgments"
            )
        if record["review_status"] == "HUMAN REVIEWED" and any(
            "PENDING HUMAN REVIEW" in judgments[model]["rationale"] for model in MODELS
        ):
            raise SchemaValidationError(
                f"{context}: HUMAN REVIEWED rationale cannot retain the pending-review marker"
            )
        if evals[case_id]["grader"]["type"] == "human_review_required" and record[
            "review_status"
        ] == "PENDING HUMAN REVIEW":
            for model in MODELS:
                if judgments[model]["outcome"] != "PENDING HUMAN REVIEW":
                    raise SchemaValidationError(
                        f"{context}: manual grader judgments must remain pending until human review"
                    )
        result[case_id] = record
        first_lines[case_id] = line_number

    expected_ids = set(evals)
    actual_ids = set(result)
    missing = sorted(expected_ids - actual_ids)
    unexpected = sorted(actual_ids - expected_ids)
    if missing or unexpected:
        parts: list[str] = []
        if missing:
            parts.append("missing gold IDs: " + ", ".join(missing))
        if unexpected:
            parts.append("unexpected gold IDs: " + ", ".join(unexpected))
        raise CoverageError("gold does not exactly cover eval IDs; " + "; ".join(parts))
    return result


def validate_inputs(
    eval_records: Iterable[dict[str, Any]],
    response_records: Iterable[dict[str, Any]],
    gold_records: Iterable[dict[str, Any]],
) -> ValidatedInputs:
    evals = validate_evals(eval_records)
    responses = validate_responses(response_records, evals)
    gold = validate_gold(gold_records, evals, responses)
    return ValidatedInputs(evals=evals, responses=responses, gold=gold)


def _format_pairs(pairs: list[tuple[str, str]]) -> str:
    limit = 12
    rendered = ", ".join(f"{case_id}/{model}" for case_id, model in pairs[:limit])
    if len(pairs) > limit:
        rendered += f", ... (+{len(pairs) - limit} more)"
    return rendered
