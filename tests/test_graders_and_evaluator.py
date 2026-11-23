"""Deterministic grader behavior and evaluator-self-audit tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sentinel.graders import grade_output
from sentinel.runner import run_evaluation
from sentinel.schema import validate_grader

from tests.support import EVALS_PATH, GOLD_PATH, RESPONSES_PATH, fixture_records


class DeterministicGraderTests(unittest.TestCase):
    def test_regex_fullmatch_rejects_prefix_suffix_and_explanatory_prose(self) -> None:
        grader = {
            "type": "regex",
            "pattern": r"^[A-Z]{3}-[0-9]{4}$",
            "match_mode": "fullmatch",
            "case_sensitive": True,
        }
        validate_grader(grader, "test grader")
        self.assertEqual(grade_output("ABC-0420", grader).status, "pass")
        for output in ("ABC-0420 extra", "id=ABC-0420", "abc-0420", "ABC-0420\n"):
            with self.subTest(output=output):
                self.assertEqual(grade_output(output, grader).status, "fail")

    def test_duplicate_keys_make_model_json_invalid(self) -> None:
        grader = {"type": "valid_json", "expected_type": "object"}
        validate_grader(grader, "test grader")
        grade = grade_output('{"answer":1,"answer":2}', grader)
        self.assertEqual(grade.status, "fail")
        self.assertIn("duplicate JSON object key 'answer'", grade.detail)

    def test_nonstandard_json_nan_is_not_valid_json(self) -> None:
        grader = {"type": "valid_json", "expected_type": "number"}
        validate_grader(grader, "test grader")
        grade = grade_output("NaN", grader)
        self.assertEqual(grade.status, "fail")
        self.assertIn("non-standard numeric constant", grade.detail)

    def test_numeric_nan_and_infinity_fail_instead_of_poisoning_metrics(self) -> None:
        grader = {
            "type": "numeric_tolerance",
            "expected": 1,
            "absolute_tolerance": 0,
            "relative_tolerance": 0,
        }
        validate_grader(grader, "test grader")
        for output in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(output=output):
                grade = grade_output(output, grader)
                self.assertEqual(grade.status, "fail")
                self.assertIn("must be finite", grade.detail)

    def test_json_structure_distinguishes_boolean_from_integer(self) -> None:
        grader = {
            "type": "json_structure",
            "required_keys": ["count"],
            "forbidden_keys": [],
            "exact_keys": True,
            "value_types": {"count": "integer"},
            "required_values": {},
        }
        validate_grader(grader, "test grader")
        self.assertEqual(grade_output('{"count":2}', grader).status, "pass")
        grade = grade_output('{"count":true}', grader)
        self.assertEqual(grade.status, "fail")
        self.assertIn("expected integer, got boolean", grade.detail)

    def test_required_json_values_do_not_use_python_true_equals_one_coercion(self) -> None:
        grader = {
            "type": "json_structure",
            "required_keys": ["value", "nested"],
            "forbidden_keys": [],
            "exact_keys": True,
            "value_types": {},
            "required_values": {"value": 1, "nested": {"enabled": True}},
        }
        validate_grader(grader, "test grader")
        self.assertEqual(
            grade_output('{"value":1,"nested":{"enabled":true}}', grader).status,
            "pass",
        )
        for output in (
            '{"value":true,"nested":{"enabled":true}}',
            '{"value":1,"nested":{"enabled":1}}',
        ):
            with self.subTest(output=output):
                grade = grade_output(output, grader)
                self.assertEqual(grade.status, "fail")
                self.assertIn("wrong values", grade.detail)


class EvaluatorAdversarialFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._temporary_directory = tempfile.TemporaryDirectory()
        output = Path(cls._temporary_directory.name) / "results"
        cls.summary = run_evaluation(
            evals_path=EVALS_PATH,
            responses_path=RESPONSES_PATH,
            gold_path=GOLD_PATH,
            out_dir=output,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls._temporary_directory.cleanup()

    def test_planted_structured_output_regressions_are_detected(self) -> None:
        structured = self.summary["dimensions"]["structured_output"]
        self.assertEqual(structured["delta"], -0.333333)
        self.assertEqual(
            structured["transitions"]["case_ids"]["regression"],
            ["so-001", "so-002"],
        )
        rows = {row["case_id"]: row for row in self.summary["case_results"]}
        self.assertEqual(rows["so-001"]["model_A"]["status"], "pass")
        self.assertEqual(rows["so-001"]["model_B"]["status"], "fail")
        self.assertIn("invalid JSON", rows["so-001"]["model_B"]["detail"])
        self.assertEqual(rows["so-002"]["model_B"]["status"], "fail")
        self.assertIn("expected integer, got string", rows["so-002"]["model_B"]["detail"])
        critical_pairs = {
            (failure["case_id"], failure["model"])
            for failure in self.summary["critical_failures"]
        }
        self.assertTrue({("so-001", "model_B"), ("so-002", "model_B")} <= critical_pairs)

    def test_aggregate_tie_masks_a_material_dimension_regression(self) -> None:
        """An overall-only evaluator would report no change and miss a critical regression."""

        self.assertEqual(self.summary["delta"], 0.0)
        self.assertEqual(self.summary["model_a"]["overall"], self.summary["model_b"]["overall"])
        self.assertEqual(self.summary["transitions"]["counts"]["regression"], 6)
        self.assertEqual(self.summary["transitions"]["counts"]["improvement"], 6)
        self.assertLess(self.summary["dimensions"]["structured_output"]["delta"], 0)
        self.assertGreater(self.summary["dimensions"]["calibrated_uncertainty"]["delta"], 0)

    def test_fixture_meets_size_dimension_and_grader_diversity_contract(self) -> None:
        dataset = self.summary["dataset"]
        self.assertGreaterEqual(dataset["case_count"], 30)
        self.assertGreaterEqual(dataset["dimension_count"], 5)
        self.assertTrue(dataset["all_cases_synthetic"])
        self.assertEqual(dataset["synthetic_case_count"], dataset["case_count"])
        self.assertEqual(
            set(dataset["grader_counts"]),
            {
                "exact_match",
                "human_review_required",
                "json_structure",
                "numeric_tolerance",
                "regex",
                "set_membership",
                "substring",
                "valid_json",
            },
        )

    def test_naive_substring_false_positive_is_exposed_by_two_checks(self) -> None:
        """Keyword presence passes a negated claim; guardrails and gold audit expose it."""

        evals, responses, _ = fixture_records()
        case = next(record for record in evals if record["case_id"] == "cu-006")
        output = next(
            record["output"]
            for record in responses
            if record["case_id"] == "cu-006" and record["model"] == "model_B"
        )
        naive = grade_output(output, case["grader"])
        self.assertEqual(naive.status, "pass")

        guarded = {
            "type": "substring",
            "required": ["insufficient evidence"],
            "forbidden": ["definitely caused"],
            "case_sensitive": False,
        }
        validate_grader(guarded, "guarded test grader")
        self.assertEqual(grade_output(output, guarded).status, "fail")

        disagreements = self.summary["gold_review"]["deterministic_label_consistency"][
            "disagreements"
        ]
        self.assertEqual(
            [(item["case_id"], item["model"]) for item in disagreements],
            [("cu-006", "model_B")],
        )
        self.assertEqual(disagreements[0]["measured_status"], "pass")
        self.assertEqual(disagreements[0]["reference_outcome"], "fail")
        self.assertIsNone(self.summary["judge_agreement"])

    def test_paired_metric_invariants_hold_globally_and_by_dimension(self) -> None:
        def assert_metrics(metrics: dict[str, object]) -> None:
            self.assertEqual(metrics["passed"] + metrics["failed"], metrics["scored"])
            self.assertEqual(
                metrics["scored"] + metrics["needs_human_review"],
                metrics["total"],
            )
            if metrics["scored"]:
                self.assertEqual(
                    metrics["overall"],
                    round(metrics["passed"] / metrics["scored"], 6),
                )

        assert_metrics(self.summary["model_a"])
        assert_metrics(self.summary["model_b"])

        transitions = self.summary["transitions"]
        self.assertEqual(sum(transitions["counts"].values()), self.summary["cases"])
        for name, count in transitions["counts"].items():
            self.assertEqual(count, len(transitions["case_ids"][name]))
        self.assertEqual(
            self.summary["model_b"]["passed"] - self.summary["model_a"]["passed"],
            transitions["counts"]["improvement"] - transitions["counts"]["regression"],
        )
        self.assertEqual(
            self.summary["paired_sign_test"]["discordant_pairs"],
            transitions["counts"]["improvement"] + transitions["counts"]["regression"],
        )

        for dimension, data in self.summary["dimensions"].items():
            with self.subTest(dimension=dimension):
                assert_metrics(data["model_A"])
                assert_metrics(data["model_B"])
                self.assertEqual(sum(data["transitions"]["counts"].values()), data["cases"])
                self.assertEqual(data["model_A"]["total"], data["cases"])
                self.assertEqual(data["model_B"]["total"], data["cases"])

        for model_key, taxonomy_key in (("model_a", "model_A"), ("model_b", "model_B")):
            self.assertEqual(
                sum(self.summary["failure_taxonomy"][taxonomy_key].values()),
                self.summary[model_key]["failed"],
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
