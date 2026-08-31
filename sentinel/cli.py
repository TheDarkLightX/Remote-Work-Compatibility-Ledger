"""Command-line interface for Sentinel."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .errors import SentinelError
from .runner import run_evaluation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m sentinel",
        description="Fail-closed deterministic LLM regression evaluation harness.",
    )
    parser.add_argument("--version", action="version", version=f"sentinel {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate = subparsers.add_parser(
        "evaluate",
        help="validate JSONL inputs and generate summary.json plus report.md",
    )
    evaluate.add_argument("--evals", required=True, type=Path, help="evaluation-case JSONL")
    evaluate.add_argument("--responses", required=True, type=Path, help="paired response JSONL")
    evaluate.add_argument("--gold", required=True, type=Path, help="provisional/reference gold JSONL")
    evaluate.add_argument("--out", required=True, type=Path, help="output directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "evaluate":
            summary = run_evaluation(
                evals_path=args.evals,
                responses_path=args.responses,
                gold_path=args.gold,
                out_dir=args.out,
            )
        else:  # argparse enforces this; retained as a defensive invariant.
            raise AssertionError(f"unhandled command {args.command!r}")
    except (SentinelError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    a = summary["model_a"]
    b = summary["model_b"]
    delta = "n/a" if summary["delta"] is None else f"{summary['delta']:+.6f}"
    print(
        "PASS: validated "
        f"{summary['cases']} cases; model_A={a['passed']}/{a['scored']}, "
        f"model_B={b['passed']}/{b['scored']}, delta={delta}"
    )
    print(f"WROTE: {args.out / 'summary.json'}")
    print(f"WROTE: {args.out / 'report.md'}")
    return 0
