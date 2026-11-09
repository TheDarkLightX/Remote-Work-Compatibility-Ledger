"""Stable Markdown rendering for measured Sentinel results."""

from __future__ import annotations

import html
from typing import Any


def _pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value * 100:.2f}%"


def _delta(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:+.2f} pp"


def _safe_text(value: str) -> str:
    """Keep data-provided prose from injecting Markdown sections or HTML."""

    return html.escape(" ".join(value.split()), quote=False).replace("|", "\\|")


def render_report(summary: dict[str, Any]) -> str:
    """Render measured facts and explicit human-owned placeholders only."""

    a = summary["model_a"]
    b = summary["model_b"]
    dataset = summary["dataset"]
    transitions = summary["transitions"]
    gold = summary["gold_review"]
    label_check = gold["deterministic_label_consistency"]
    authoritative = summary["authoritative_gold_scoring"]

    if gold["all_human_reviewed"]:
        review_banner = [
            "> **SYNTHETIC FIXTURES — GOLD RECORDS MARKED HUMAN REVIEWED.** The cases and initial",
            "> conditions were AI-drafted; every response-bound gold record is marked HUMAN REVIEWED.",
            "> These results still do not measure named production models.",
        ]
    else:
        review_banner = [
            "> **SYNTHETIC FIXTURES — MACHINE MEASUREMENT ONLY.** The expected conditions and",
            "> provisional labels were drafted with AI and remain **PENDING HUMAN REVIEW**. These",
            "> results do not measure named production models.",
        ]

    lines: list[str] = [
        "# EVAL-001 Automated Measurement Report",
        "",
        *review_banner,
        "",
        "## Decision status",
        "",
        "**Dana's final decision: PENDING HUMAN REVIEW.** The harness does not choose `ship B`,",
        "`do not ship`, or `evidence insufficient` on Dana's behalf.",
        "",
        "## Measured result",
        "",
        "| Metric | model_A | model_B | B − A |",
        "| --- | ---: | ---: | ---: |",
        (
            f"| Deterministic pass rate | {a['passed']}/{a['scored']} ({_pct(a['overall'])}) | "
            f"{b['passed']}/{b['scored']} ({_pct(b['overall'])}) | {_delta(summary['delta'])} |"
        ),
        (
            f"| Pending manual cases | {a['needs_human_review']} | "
            f"{b['needs_human_review']} | n/a |"
        ),
        "",
        (
            f"The suite contains **{dataset['case_count']} cases** across "
            f"**{dataset['dimension_count']} dimensions**. "
            f"{dataset['automatically_scorable_cases']} cases are automatically scorable and "
            f"{dataset['human_review_required_cases']} is explicitly excluded pending human judgment."
        ),
        "",
        "## Dimension movement",
        "",
        "| Dimension | Cases (scored) | model_A | model_B | B − A |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for dimension, metrics in summary["dimensions"].items():
        ma = metrics["model_A"]
        mb = metrics["model_B"]
        lines.append(
            f"| `{dimension}` | {metrics['cases']} ({ma['scored']}) | "
            f"{ma['passed']}/{ma['scored']} ({_pct(ma['overall'])}) | "
            f"{mb['passed']}/{mb['scored']} ({_pct(mb['overall'])}) | "
            f"{_delta(metrics['delta'])} |"
        )

    lines.extend(
        [
            "",
            "## Paired changes",
            "",
            f"- B regressions (A pass → B fail): **{transitions['counts']['regression']}** — "
            + ", ".join(f"`{case_id}`" for case_id in transitions["case_ids"]["regression"]),
            f"- B improvements (A fail → B pass): **{transitions['counts']['improvement']}** — "
            + ", ".join(f"`{case_id}`" for case_id in transitions["case_ids"]["improvement"]),
            f"- Both pass: **{transitions['counts']['both_pass']}**",
            f"- Both fail: **{transitions['counts']['both_fail']}**",
            f"- Needs human review: **{transitions['counts']['needs_human_review']}**",
            "",
            "The exact paired sign test is descriptive only: "
            f"p = {summary['paired_sign_test']['two_sided_p_value']:.6f} across "
            f"{summary['paired_sign_test']['discordant_pairs']} discordant pairs. "
            "Because these fixtures were deliberately constructed rather than randomly sampled, "
            "this is not evidence about a production population.",
            "",
            "## Planted critical case failures",
            "",
        ]
    )
    if summary["critical_failures"]:
        for failure in summary["critical_failures"]:
            lines.append(
                f"- `{failure['case_id']}` / `{failure['model']}` — "
                f"`{failure['failure_type']}` in `{failure['dimension']}`; grader cause "
                f"`{failure['grader_failure_code']}`. Criterion: "
                f"{_safe_text(failure['success_criterion'])} Observed: "
                f"{_safe_text(failure['detail'])}"
            )
    else:
        lines.append("- None measured.")
    lines.extend(
        [
            "",
            "These are case-level severity flags in the synthetic fixture, not rubric-level critical failures.",
            "",
            "## Declared domain failure taxonomy",
            "",
            "| Model | Failure type | Count |",
            "| --- | --- | ---: |",
        ]
    )
    for model in ("model_A", "model_B"):
        for failure_type, count in summary["failure_taxonomy"][model].items():
            lines.append(f"| `{model}` | `{failure_type}` | {count} |")

    lines.extend(
        [
            "",
            "## Observed grader-failure causes",
            "",
            "This second taxonomy records what the deterministic check actually observed; it is "
            "kept separate from the case author's declared domain failure category.",
            "",
            "| Model | Grader cause | Count |",
            "| --- | --- | ---: |",
        ]
    )
    for model in ("model_A", "model_B"):
        for reason_code, count in summary["grader_failure_taxonomy"][model].items():
            lines.append(f"| `{model}` | `{reason_code}` | {count} |")

    lines.extend(
        [
            "",
            "## Evaluator audit",
            "",
            (
                (
                    "The deterministic grader and response-bound records marked HUMAN REVIEWED "
                    if gold["all_human_reviewed"]
                    else "The deterministic grader and AI-drafted provisional labels "
                )
                + f"were comparable on {label_check['comparable_judgments']} model/case judgments. "
                + f"They disagreed on **{len(label_check['disagreements'])}**. "
                + (
                    "This is recorded judge agreement, not independent verification."
                    if gold["all_human_reviewed"]
                    else "This is draft consistency—not human judge agreement."
                )
            ),
            "",
        ]
    )
    if label_check["disagreements"]:
        for disagreement in label_check["disagreements"]:
            lines.append(
                f"- `{disagreement['case_id']}` / `{disagreement['model']}`: deterministic grader "
                f"measured **{disagreement['measured_status']}**, reference label says "
                f"**{disagreement['reference_outcome']}**. "
                f"{_safe_text(disagreement['reference_rationale'])}"
            )
    else:
        lines.append("- No draft-label inconsistencies were measured.")

    lines.extend(["", "Manual-only boundaries:", ""])
    if summary["boundary_cases"]:
        for boundary in summary["boundary_cases"]:
            lines.append(
                f"- `{boundary['case_id']}` (`{boundary['dimension']}`): "
                f"{_safe_text(boundary['reason'])}"
            )
    else:
        lines.append("- None.")

    if gold["all_human_reviewed"]:
        lines.extend(
            [
                "",
                f"Deterministic-vs-recorded-gold agreement: **{_pct(summary['judge_agreement'])}**.",
                "",
                "### Gold-authoritative result",
                "",
                "| Metric | model_A | model_B | B − A |",
                "| --- | ---: | ---: | ---: |",
                (
                    f"| Human-reviewed gold pass rate | "
                    f"{authoritative['model_a']['passed']}/{authoritative['model_a']['scored']} "
                    f"({_pct(authoritative['model_a']['overall'])}) | "
                    f"{authoritative['model_b']['passed']}/{authoritative['model_b']['scored']} "
                    f"({_pct(authoritative['model_b']['overall'])}) | "
                    f"{_delta(authoritative['delta'])} |"
                ),
                "",
                authoritative["warning"],
            ]
        )
    else:
        lines.extend(
            [
                "",
                "`judge_agreement` remains `null`: "
                f"{gold['human_reviewed_cases']}/{summary['cases']} gold records are human-reviewed.",
                "",
                "### Gold-authoritative result",
                "",
                "Withheld: every response-bound gold record must be human-reviewed first. "
                "Automated pass rates above are measurements, not the final gold-authoritative score.",
            ]
        )

    gold_limitation = (
        "- The cases and initial conditions were AI-drafted; recorded human review does not turn "
        "this synthetic suite into a production sample."
        if gold["all_human_reviewed"]
        else "- The expected conditions, outputs, and provisional labels were AI-drafted; Dana has "
        "not approved them."
    )
    gold_task = (
        "- [x] Every response-bound gold record is marked HUMAN REVIEWED in the input; preserve "
        "the candidate's underlying review notes."
        if gold["all_human_reviewed"]
        else "- [ ] Review and approve or correct every expected condition and gold label."
    )

    lines.extend(
        [
            "",
            "## Known engineering limitations",
            "",
            "- The suite is small, synthetic, and deliberately balanced; it does not estimate real-model quality.",
            "- Deterministic graders test declared surface conditions and can miss semantics, negation, or gaming.",
            gold_limitation,
            "- Static SHA-256 bindings catch ordinary swaps/staleness, but not coordinated falsification "
            "of IDs, hashes, and provenance at the source.",
            "- Regex grader configurations are trusted inputs; Python regular expressions have no timeout "
            "and should not accept arbitrary untrusted patterns in a hosted service.",
            "- No latency, cost, repeated-sampling variance, data drift, or live model API behavior is measured.",
            "- A same-worktree deterministic rerun is not a candidate-confirmed clean-checkout replay.",
            "",
            "## Human-owned decision checkpoint",
            "",
            "Dana must personally complete these before any completion or portfolio-ready claim:",
            "",
            gold_task,
            "- [ ] Inspect at least 10 disagreement, regression, improvement, or boundary cases.",
            "- [ ] Identify at least one case where automation was misleading or insufficient.",
            "- [ ] Decide: `ship model B`, `do not ship`, or `evidence insufficient`.",
            "- [ ] State the strongest defensible claim and its limitations.",
            "- [ ] Complete the oral defense without AI assistance.",
            "- [ ] Confirm reproduction from a clean checkout.",
            "- [ ] Approve the final rubric score and portfolio status.",
            "",
            "---",
            "",
            "Generated deterministically by the Sentinel harness from the committed JSONL inputs. "
            "No timestamp is embedded so identical inputs produce identical bytes.",
            "",
        ]
    )
    return "\n".join(lines)
