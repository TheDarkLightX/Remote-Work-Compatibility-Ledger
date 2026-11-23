"""Transparent deterministic graders used by the regression harness."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

from .io import strict_json_loads


@dataclass(frozen=True)
class Grade:
    status: str
    score: int | None
    detail: str
    reason_code: str | None


def _passed(detail: str) -> Grade:
    return Grade(status="pass", score=1, detail=detail, reason_code=None)


def _failed(reason_code: str, detail: str) -> Grade:
    return Grade(status="fail", score=0, detail=detail, reason_code=reason_code)


def _normalize(text: str, settings: dict[str, bool] | None) -> str:
    if not settings:
        return text
    result = text
    if settings.get("strip", False):
        result = result.strip()
    if settings.get("collapse_whitespace", False):
        result = " ".join(result.split())
    if settings.get("casefold", False):
        result = result.casefold()
    return result


def _json_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    raise TypeError(f"unsupported decoded JSON type {type(value).__name__}")


def _matches_json_type(value: Any, expected: str) -> bool:
    actual = _json_type(value)
    if expected == "number":
        return actual in {"integer", "number"}
    return actual == expected


def _json_values_equal(actual: Any, expected: Any) -> bool:
    """Compare JSON values without Python's ``True == 1`` coercion."""

    if actual is None or expected is None:
        return actual is expected
    if isinstance(actual, bool) or isinstance(expected, bool):
        return isinstance(actual, bool) and isinstance(expected, bool) and actual == expected
    if isinstance(actual, (int, float)) or isinstance(expected, (int, float)):
        return (
            isinstance(actual, (int, float))
            and isinstance(expected, (int, float))
            and actual == expected
        )
    if isinstance(actual, str) or isinstance(expected, str):
        return isinstance(actual, str) and isinstance(expected, str) and actual == expected
    if isinstance(actual, list) or isinstance(expected, list):
        return (
            isinstance(actual, list)
            and isinstance(expected, list)
            and len(actual) == len(expected)
            and all(_json_values_equal(left, right) for left, right in zip(actual, expected))
        )
    if isinstance(actual, dict) or isinstance(expected, dict):
        return (
            isinstance(actual, dict)
            and isinstance(expected, dict)
            and set(actual) == set(expected)
            and all(_json_values_equal(actual[key], expected[key]) for key in actual)
        )
    return False


def _decode_model_json(output: str) -> tuple[bool, Any | str]:
    try:
        return True, strict_json_loads(output)
    except (json.JSONDecodeError, ValueError, RecursionError) as exc:
        # Expected parse/resource failures are model-output data. Unexpected
        # programming faults must propagate instead of being mislabeled.
        return False, str(exc)


def grade_output(output: str, grader: dict[str, Any]) -> Grade:
    """Grade one output after the grader configuration has been validated."""

    grader_type = grader["type"]

    if grader_type == "exact_match":
        actual = _normalize(output, grader.get("normalization"))
        expected = _normalize(grader["expected"], grader.get("normalization"))
        if actual == expected:
            return _passed("exact match")
        return _failed("exact_mismatch", f"exact mismatch: expected {grader['expected']!r}")

    if grader_type == "substring":
        actual = output if grader["case_sensitive"] else output.casefold()
        required = grader["required"]
        forbidden = grader["forbidden"]
        comparable_required = required if grader["case_sensitive"] else [x.casefold() for x in required]
        comparable_forbidden = forbidden if grader["case_sensitive"] else [x.casefold() for x in forbidden]
        missing = [original for original, token in zip(required, comparable_required) if token not in actual]
        present_forbidden = [
            original for original, token in zip(forbidden, comparable_forbidden) if token in actual
        ]
        if not missing and not present_forbidden:
            return _passed("all required substrings present; no forbidden substrings present")
        parts: list[str] = []
        if missing:
            parts.append("missing required: " + ", ".join(repr(x) for x in missing))
        if present_forbidden:
            parts.append("contains forbidden: " + ", ".join(repr(x) for x in present_forbidden))
        return _failed("substring_constraint_failure", "; ".join(parts))

    if grader_type == "valid_json":
        ok, decoded = _decode_model_json(output)
        if not ok:
            return _failed("invalid_json", f"invalid JSON: {decoded}")
        expected_type = grader["expected_type"]
        if expected_type != "any" and not _matches_json_type(decoded, expected_type):
            return _failed(
                "json_type_mismatch",
                f"JSON type mismatch: expected {expected_type}, got {_json_type(decoded)}"
            )
        return _passed(
            "valid JSON" if expected_type == "any" else f"valid JSON {expected_type}"
        )

    if grader_type == "json_structure":
        ok, decoded = _decode_model_json(output)
        if not ok:
            return _failed("invalid_json", f"invalid JSON: {decoded}")
        if not isinstance(decoded, dict):
            return _failed(
                "json_type_mismatch", f"expected JSON object, got {_json_type(decoded)}"
            )
        actual_keys = set(decoded)
        required_keys = set(grader["required_keys"])
        forbidden_keys = set(grader["forbidden_keys"])
        missing = sorted(required_keys - actual_keys)
        present_forbidden = sorted(forbidden_keys & actual_keys)
        extra = sorted(actual_keys - required_keys) if grader["exact_keys"] else []
        wrong_types = sorted(
            key
            for key, expected_type in grader["value_types"].items()
            if key in decoded and not _matches_json_type(decoded[key], expected_type)
        )
        wrong_values = sorted(
            key
            for key, expected_value in grader["required_values"].items()
            if key in decoded and not _json_values_equal(decoded[key], expected_value)
        )
        if not (missing or present_forbidden or extra or wrong_types or wrong_values):
            return _passed("JSON object satisfies key, type, and value constraints")
        parts: list[str] = []
        if missing:
            parts.append("missing keys: " + ", ".join(missing))
        if present_forbidden:
            parts.append("forbidden keys: " + ", ".join(present_forbidden))
        if extra:
            parts.append("extra keys: " + ", ".join(extra))
        if wrong_types:
            rendered = ", ".join(
                f"{key} (expected {grader['value_types'][key]}, got {_json_type(decoded[key])})"
                for key in wrong_types
            )
            parts.append("wrong types: " + rendered)
        if wrong_values:
            rendered = ", ".join(
                f"{key} (expected {grader['required_values'][key]!r})" for key in wrong_values
            )
            parts.append("wrong values: " + rendered)
        if missing or present_forbidden or extra:
            reason_code = "json_key_constraint_failure"
        elif wrong_types:
            reason_code = "json_type_constraint_failure"
        else:
            reason_code = "json_value_constraint_failure"
        return _failed(reason_code, "; ".join(parts))

    if grader_type == "numeric_tolerance":
        try:
            actual = Decimal(output.strip())
            expected = Decimal(str(grader["expected"]))
            absolute = Decimal(str(grader["absolute_tolerance"]))
            relative = Decimal(str(grader["relative_tolerance"]))
        except (InvalidOperation, ValueError) as exc:
            return _failed("invalid_numeric", f"not a plain numeric value: {exc}")
        if not actual.is_finite():
            return _failed("invalid_numeric", "numeric output must be finite")
        error = abs(actual - expected)
        allowed = max(absolute, relative * abs(expected))
        if error <= allowed:
            return _passed(f"numeric error {error} within tolerance {allowed}")
        return _failed(
            "numeric_out_of_tolerance", f"numeric error {error} exceeds tolerance {allowed}"
        )

    if grader_type == "set_membership":
        actual = output.strip() if grader["strip"] else output
        allowed = [item.strip() for item in grader["allowed"]] if grader["strip"] else list(
            grader["allowed"]
        )
        if not grader["case_sensitive"]:
            actual = actual.casefold()
            allowed = [item.casefold() for item in allowed]
        if actual in allowed:
            return _passed("output is in the allowed set")
        return _failed(
            "set_membership_failure",
            "output is not in allowed set: " + ", ".join(repr(x) for x in grader["allowed"]),
        )

    if grader_type == "regex":
        flags = 0 if grader["case_sensitive"] else re.IGNORECASE
        pattern = re.compile(grader["pattern"], flags=flags)
        match = pattern.fullmatch(output) if grader["match_mode"] == "fullmatch" else pattern.search(output)
        if match is not None:
            return _passed(f"regex {grader['match_mode']} succeeded")
        return _failed(
            "regex_mismatch",
            f"regex {grader['match_mode']} failed for pattern {grader['pattern']!r}",
        )

    if grader_type == "human_review_required":
        return Grade(
            status="needs_human_review",
            score=None,
            detail=grader["reason"],
            reason_code=None,
        )

    raise AssertionError(f"validated grader type is not implemented: {grader_type}")
