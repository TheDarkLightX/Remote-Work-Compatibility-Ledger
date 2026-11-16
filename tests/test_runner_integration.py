"""End-to-end reproducibility and transactional-output tests."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from sentinel.errors import JsonlParseError
from sentinel.runner import run_evaluation

from tests.support import (
    EVALS_PATH,
    GOLD_PATH,
    REPOSITORY_ROOT,
    RESPONSES_PATH,
    fixture_records,
    write_records,
)


class RunnerIntegrationTests(unittest.TestCase):
    def test_cli_runs_end_to_end_from_repository_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "results"
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "sentinel",
                    "evaluate",
                    "--evals",
                    str(EVALS_PATH),
                    "--responses",
                    str(RESPONSES_PATH),
                    "--gold",
                    str(GOLD_PATH),
                    "--out",
                    str(output),
                ],
                cwd=REPOSITORY_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("PASS: validated 37 cases", completed.stdout)
            self.assertEqual(completed.stderr, "")
            self.assertTrue((output / "summary.json").is_file())
            self.assertTrue((output / "report.md").is_file())

    def test_cli_reports_malformed_jsonl_as_failure_without_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bad_evals = root / "bad-evals.jsonl"
            bad_evals.write_text('{"case_id":}\n', encoding="utf-8")
            output = root / "results"
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "sentinel",
                    "evaluate",
                    "--evals",
                    str(bad_evals),
                    "--responses",
                    str(RESPONSES_PATH),
                    "--gold",
                    str(GOLD_PATH),
                    "--out",
                    str(output),
                ],
                cwd=REPOSITORY_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertEqual(completed.stdout, "")
            self.assertIn("ERROR:", completed.stderr)
            self.assertIn("bad-evals.jsonl:1", completed.stderr)
            self.assertFalse(output.exists())

    def test_repeated_runs_produce_byte_identical_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first"
            second = root / "second"
            first_summary = run_evaluation(
                evals_path=EVALS_PATH,
                responses_path=RESPONSES_PATH,
                gold_path=GOLD_PATH,
                out_dir=first,
            )
            second_summary = run_evaluation(
                evals_path=EVALS_PATH,
                responses_path=RESPONSES_PATH,
                gold_path=GOLD_PATH,
                out_dir=second,
            )
            self.assertEqual(first_summary, second_summary)
            self.assertEqual(
                (first / "summary.json").read_bytes(),
                (second / "summary.json").read_bytes(),
            )
            self.assertEqual(
                (first / "report.md").read_bytes(),
                (second / "report.md").read_bytes(),
            )

    def test_shuffled_input_order_does_not_change_measured_results_or_report(self) -> None:
        evals, responses, gold = fixture_records()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical_out = root / "canonical-results"
            shuffled_out = root / "shuffled-results"
            canonical = run_evaluation(
                evals_path=EVALS_PATH,
                responses_path=RESPONSES_PATH,
                gold_path=GOLD_PATH,
                out_dir=canonical_out,
            )

            shuffled_evals = root / "evals.jsonl"
            shuffled_responses = root / "responses.jsonl"
            shuffled_gold = root / "gold.jsonl"
            write_records(shuffled_evals, list(reversed(evals)))
            # Use different deterministic permutations, not only one shared reversal.
            write_records(shuffled_responses, responses[1::2] + responses[::2])
            write_records(shuffled_gold, gold[::2] + gold[1::2])
            shuffled = run_evaluation(
                evals_path=shuffled_evals,
                responses_path=shuffled_responses,
                gold_path=shuffled_gold,
                out_dir=shuffled_out,
            )

            # Source-byte hashes correctly differ when line order changes. Everything measured
            # from those records must remain identical and deterministically ordered.
            canonical_without_hashes = copy.deepcopy(canonical)
            shuffled_without_hashes = copy.deepcopy(shuffled)
            canonical_without_hashes.pop("input_sha256")
            shuffled_without_hashes.pop("input_sha256")
            self.assertEqual(canonical_without_hashes, shuffled_without_hashes)
            self.assertNotEqual(canonical["input_sha256"], shuffled["input_sha256"])
            self.assertEqual(
                (canonical_out / "report.md").read_bytes(),
                (shuffled_out / "report.md").read_bytes(),
            )
            case_ids = [row["case_id"] for row in shuffled["case_results"]]
            self.assertEqual(case_ids, sorted(case_ids))
            self.assertEqual(list(shuffled["dimensions"]), sorted(shuffled["dimensions"]))

    def test_invalid_rerun_preserves_last_known_good_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "results"
            run_evaluation(
                evals_path=EVALS_PATH,
                responses_path=RESPONSES_PATH,
                gold_path=GOLD_PATH,
                out_dir=output,
            )
            original_summary = (output / "summary.json").read_bytes()
            original_report = (output / "report.md").read_bytes()

            corrupted_responses = root / "responses-corrupted.jsonl"
            corrupted_responses.write_text(
                RESPONSES_PATH.read_text(encoding="utf-8") + "{malformed\n",
                encoding="utf-8",
                newline="\n",
            )
            with self.assertRaises(JsonlParseError):
                run_evaluation(
                    evals_path=EVALS_PATH,
                    responses_path=corrupted_responses,
                    gold_path=GOLD_PATH,
                    out_dir=output,
                )

            self.assertEqual((output / "summary.json").read_bytes(), original_summary)
            self.assertEqual((output / "report.md").read_bytes(), original_report)
            self.assertEqual(
                sorted(path.name for path in output.iterdir()),
                ["report.md", "summary.json"],
            )

    def test_machine_report_tracks_measured_summary_and_keeps_decision_pending(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "results"
            summary = run_evaluation(
                evals_path=EVALS_PATH,
                responses_path=RESPONSES_PATH,
                gold_path=GOLD_PATH,
                out_dir=output,
            )
            persisted = json.loads((output / "summary.json").read_text(encoding="utf-8"))
            report = (output / "report.md").read_text(encoding="utf-8")
            self.assertEqual(persisted, summary)
            self.assertIsNone(summary["final_decision"])
            self.assertIn("30/36 (83.33%)", report)
            self.assertIn("`structured_output`", report)
            self.assertIn("-33.33 pp", report)
            self.assertIn("Dana's final decision: PENDING HUMAN REVIEW", report)
            self.assertIn("`cu-006` / `model_B`", report)

    def test_human_reviewed_gold_enables_separate_authoritative_metrics(self) -> None:
        evals, responses, gold = fixture_records()
        del evals, responses  # The committed files remain the response/hash authority.
        for record in gold:
            record["review_status"] = "HUMAN REVIEWED"
            record["reviewed_by"] = "Test Reviewer"
            record["reviewed_at"] = "2030-01-01T00:00:00Z"
            for model in ("model_A", "model_B"):
                record["judgments"][model]["rationale"] = (
                    "Test-only simulated human-reviewed rationale."
                )
            if record["case_id"] == "cu-007":
                record["judgments"]["model_A"].update(
                    {
                        "outcome": "fail",
                        "failure_type": "ambiguous_policy_boundary",
                        "rationale": "Test-only simulated human judgment.",
                    }
                )
                record["judgments"]["model_B"].update(
                    {
                        "outcome": "pass",
                        "failure_type": None,
                        "rationale": "Test-only simulated human judgment.",
                    }
                )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reviewed_gold = root / "gold.jsonl"
            write_records(reviewed_gold, gold)
            output = root / "results"
            summary = run_evaluation(
                evals_path=EVALS_PATH,
                responses_path=RESPONSES_PATH,
                gold_path=reviewed_gold,
                out_dir=output,
            )
            report = (output / "report.md").read_text(encoding="utf-8")

        authoritative = summary["authoritative_gold_scoring"]
        self.assertEqual(authoritative["status"], "AVAILABLE")
        self.assertEqual(authoritative["model_a"]["scored"], 37)
        self.assertEqual(authoritative["model_b"]["scored"], 37)
        self.assertIsNotNone(summary["judge_agreement"])
        self.assertIn("GOLD RECORDS MARKED HUMAN REVIEWED", report)
        self.assertIn("Human-reviewed gold pass rate", report)
        self.assertNotIn("`judge_agreement` remains `null`", report)
        self.assertIn("Dana's final decision: PENDING HUMAN REVIEW", report)

    def test_report_collapses_and_escapes_data_provided_markdown(self) -> None:
        _, _, gold = fixture_records()
        gold[0]["judgments"]["model_A"]["outcome"] = "fail"
        gold[0]["judgments"]["model_A"]["failure_type"] = "factual_mismatch"
        gold[0]["judgments"]["model_A"]["rationale"] = (
            "Injected\n## Fake verified section\n- [x] verified <script>alert(1)</script> | pipe"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            gold_path = root / "gold.jsonl"
            write_records(gold_path, gold)
            output = root / "results"
            run_evaluation(
                evals_path=EVALS_PATH,
                responses_path=RESPONSES_PATH,
                gold_path=gold_path,
                out_dir=output,
            )
            report = (output / "report.md").read_text(encoding="utf-8")

        self.assertNotIn("\n## Fake verified section", report)
        self.assertNotIn("<script>", report)
        self.assertIn("&lt;script&gt;", report)
        self.assertIn("\\| pipe", report)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
