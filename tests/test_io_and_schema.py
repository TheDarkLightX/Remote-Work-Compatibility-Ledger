"""Fail-closed parsing, schema, coverage, and alignment tests."""

from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from sentinel.errors import (
    AlignmentError,
    CoverageError,
    DuplicateIDError,
    GraderConfigurationError,
    JsonlParseError,
    SchemaValidationError,
)
from sentinel.io import load_jsonl, strict_json_loads
from sentinel.schema import validate_evals, validate_gold, validate_inputs, validate_responses

from tests.support import fixture_records


class StrictJsonlTests(unittest.TestCase):
    def assert_jsonl_rejected(self, raw: bytes, message_pattern: str) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.jsonl"
            path.write_bytes(raw)
            with self.assertRaisesRegex(JsonlParseError, message_pattern):
                load_jsonl(path, "test-input")

    def test_malformed_json_is_rejected_with_line_context(self) -> None:
        self.assert_jsonl_rejected(
            b'{"case_id":"ok"}\n{"case_id":}\n',
            r"test-input: .*:2:.*Expecting value",
        )

    def test_empty_file_is_rejected(self) -> None:
        self.assert_jsonl_rejected(b"", r"is empty")

    def test_blank_jsonl_line_is_rejected(self) -> None:
        self.assert_jsonl_rejected(
            b'{"case_id":"one"}\n   \n{"case_id":"two"}\n',
            r":2: blank JSONL lines are not allowed",
        )

    def test_non_object_record_is_rejected(self) -> None:
        self.assert_jsonl_rejected(b'["not", "an", "object"]\n', r"must be an object")

    def test_duplicate_json_object_keys_are_rejected_at_any_depth(self) -> None:
        self.assert_jsonl_rejected(
            b'{"case_id":"one","nested":{"x":1,"x":2}}\n',
            r"duplicate JSON object key 'x'",
        )
        with self.assertRaisesRegex(ValueError, r"duplicate JSON object key 'a'"):
            strict_json_loads('{"a":1,"a":2}')

    def test_nonstandard_nan_is_rejected(self) -> None:
        self.assert_jsonl_rejected(b'{"score":NaN}\n', r"numeric constant 'NaN' is not allowed")

    def test_invalid_utf8_is_rejected(self) -> None:
        self.assert_jsonl_rejected(b'{"case_id":"\xff"}\n', r"not valid UTF-8")


class SchemaCoverageAndAlignmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.evals, self.responses, self.gold = fixture_records()

    def test_committed_fixture_validates_exact_pair_coverage(self) -> None:
        validated = validate_inputs(self.evals, self.responses, self.gold)
        self.assertEqual(len(validated.evals), 37)
        self.assertEqual(len(validated.responses), 74)
        self.assertEqual(len(validated.gold), 37)
        self.assertEqual(
            set(validated.responses),
            {
                (case_id, model)
                for case_id in validated.evals
                for model in ("model_A", "model_B")
            },
        )

    def test_duplicate_eval_case_id_is_rejected(self) -> None:
        self.evals.append(copy.deepcopy(self.evals[0]))
        with self.assertRaisesRegex(DuplicateIDError, r"duplicate case_id 'fg-001'"):
            validate_evals(self.evals)

    def test_duplicate_response_pair_is_rejected(self) -> None:
        self.responses.append(copy.deepcopy(self.responses[0]))
        evals = validate_evals(self.evals)
        with self.assertRaisesRegex(DuplicateIDError, r"duplicate response pair"):
            validate_responses(self.responses, evals)

    def test_duplicate_gold_case_id_is_rejected(self) -> None:
        self.gold.append(copy.deepcopy(self.gold[0]))
        evals = validate_evals(self.evals)
        responses = validate_responses(self.responses, evals)
        with self.assertRaisesRegex(DuplicateIDError, r"duplicate case_id 'fg-001'"):
            validate_gold(self.gold, evals, responses)

    def test_missing_model_output_is_rejected(self) -> None:
        removed = self.responses.pop()
        with self.assertRaisesRegex(
            CoverageError,
            rf"missing response pairs: {removed['case_id']}/{removed['model']}",
        ):
            validate_inputs(self.evals, self.responses, self.gold)

    def test_unexpected_case_id_is_rejected(self) -> None:
        unexpected = copy.deepcopy(self.responses[0])
        unexpected.update(
            {
                "case_id": "unknown-001",
                "response_id": "unknown-001::model_A",
            }
        )
        self.responses.append(unexpected)
        with self.assertRaisesRegex(CoverageError, r"unexpected response pairs: unknown-001/model_A"):
            validate_inputs(self.evals, self.responses, self.gold)

    def test_unsupported_model_is_rejected_before_coverage_is_computed(self) -> None:
        self.responses[0]["model"] = "model_C"
        self.responses[0]["response_id"] = "fg-001::model_C"
        with self.assertRaisesRegex(
            SchemaValidationError,
            r"model must be exactly model_A or model_B; got 'model_C'",
        ):
            validate_inputs(self.evals, self.responses, self.gold)

    def test_response_id_detects_case_model_misalignment(self) -> None:
        self.responses[0]["response_id"] = "fg-001::model_B"
        with self.assertRaisesRegex(
            AlignmentError,
            r"response_id .* does not match case/model binding 'fg-001::model_A'",
        ):
            validate_inputs(self.evals, self.responses, self.gold)

    def test_response_eval_fingerprint_detects_swapped_or_stale_case(self) -> None:
        self.responses[0]["eval_sha256"] = self.responses[2]["eval_sha256"]
        with self.assertRaisesRegex(
            AlignmentError,
            r"fingerprint mismatch for 'fg-001'; response may be swapped or stale",
        ):
            validate_inputs(self.evals, self.responses, self.gold)

    def test_gold_eval_fingerprint_detects_swapped_or_stale_case(self) -> None:
        self.gold[0]["eval_sha256"] = self.gold[1]["eval_sha256"]
        with self.assertRaisesRegex(
            AlignmentError,
            r"fingerprint mismatch for 'fg-001'; gold may be swapped or stale",
        ):
            validate_inputs(self.evals, self.responses, self.gold)

    def test_gold_response_fingerprint_detects_changed_or_swapped_output(self) -> None:
        self.responses[0]["output"] = "changed after provisional review"
        with self.assertRaisesRegex(
            AlignmentError,
            r"response fingerprint mismatch for 'fg-001'; gold may bind a stale or swapped output",
        ):
            validate_inputs(self.evals, self.responses, self.gold)

    def test_response_with_unknown_field_fails_closed(self) -> None:
        self.responses[0]["latency_ms"] = 12
        with self.assertRaisesRegex(SchemaValidationError, r"unknown keys: latency_ms"):
            validate_inputs(self.evals, self.responses, self.gold)


class CorruptedGraderConfigurationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base_eval = fixture_records()[0][0]

    def assert_grader_rejected(self, grader: object, message_pattern: str) -> None:
        record = copy.deepcopy(self.base_eval)
        record["grader"] = grader
        with self.assertRaisesRegex(GraderConfigurationError, message_pattern):
            validate_evals([record])

    def test_corrupted_expected_conditions_are_rejected(self) -> None:
        corruptions: list[tuple[str, object, str]] = [
            (
                "unknown grader",
                {"type": "vibes"},
                r"unknown grader 'vibes'",
            ),
            (
                "wrong exact expected type",
                {"type": "exact_match", "expected": 1998},
                r"expected must be a string",
            ),
            (
                "contradictory substrings",
                {
                    "type": "substring",
                    "required": ["Token"],
                    "forbidden": ["token"],
                    "case_sensitive": False,
                },
                r"requires and forbids the same substring",
            ),
            (
                "invalid JSON type",
                {"type": "valid_json", "expected_type": "mapping"},
                r"expected_type must be one of",
            ),
            (
                "unbound structural type key",
                {
                    "type": "json_structure",
                    "required_keys": ["id"],
                    "forbidden_keys": [],
                    "exact_keys": True,
                    "value_types": {"count": "integer"},
                    "required_values": {},
                },
                r"value_types key 'count' must also be required",
            ),
            (
                "structural value contradicts declared type",
                {
                    "type": "json_structure",
                    "required_keys": ["count"],
                    "forbidden_keys": [],
                    "exact_keys": True,
                    "value_types": {"count": "integer"},
                    "required_values": {"count": "2"},
                },
                r"required_values\['count'\] contradicts declared type 'integer'",
            ),
            (
                "negative numeric tolerance",
                {
                    "type": "numeric_tolerance",
                    "expected": 1,
                    "absolute_tolerance": -0.1,
                    "relative_tolerance": 0,
                },
                r"tolerances must be non-negative",
            ),
            (
                "nonfinite expected numeric value",
                {
                    "type": "numeric_tolerance",
                    "expected": float("nan"),
                    "absolute_tolerance": 0,
                    "relative_tolerance": 0,
                },
                r"expected must be a finite number",
            ),
            (
                "normalized enum collision",
                {
                    "type": "set_membership",
                    "allowed": ["YES", "yes"],
                    "case_sensitive": False,
                    "strip": True,
                },
                r"duplicates after configured normalization",
            ),
            (
                "invalid regex",
                {
                    "type": "regex",
                    "pattern": "[",
                    "match_mode": "fullmatch",
                    "case_sensitive": True,
                },
                r"pattern is invalid",
            ),
            (
                "empty human review reason",
                {"type": "human_review_required", "reason": "   "},
                r"reason must be a non-empty string",
            ),
        ]
        for name, grader, pattern in corruptions:
            with self.subTest(name=name):
                self.assert_grader_rejected(grader, pattern)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
