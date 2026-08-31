#!/usr/bin/env python3
"""Minimal dependency-free validator for ledger receipt.json files.

This intentionally checks the core invariants without pretending to be a
complete JSON Schema implementation. The canonical format is defined in
schemas/receipt-v1.schema.json.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = {
    "schema_version",
    "benchmark_id",
    "submission_id",
    "evidence_mode",
    "candidate",
    "ai_disclosure",
    "reproduce",
    "status",
}
MODES = {"U", "A", "V"}
STATUSES = {
    "draft",
    "completed",
    "replayed",
    "portfolio-ready",
    "externally-verified",
}
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def fail(message: str) -> None:
    raise ValueError(message)


def validate(data: object) -> list[str]:
    if not isinstance(data, dict):
        fail("receipt root must be an object")

    missing = sorted(REQUIRED - data.keys())
    if missing:
        fail(f"missing required keys: {', '.join(missing)}")

    if data["schema_version"] != "1.0":
        fail("schema_version must be '1.0'")
    if data["evidence_mode"] not in MODES:
        fail("evidence_mode must be U, A, or V")
    if data["status"] not in STATUSES:
        fail("invalid status")

    for key in ("benchmark_id", "submission_id", "candidate"):
        if not isinstance(data[key], str) or not data[key].strip():
            fail(f"{key} must be a non-empty string")

    disclosure = data["ai_disclosure"]
    if not isinstance(disclosure, dict) or not isinstance(disclosure.get("used"), bool):
        fail("ai_disclosure.used must be boolean")

    reproduce = data["reproduce"]
    if not isinstance(reproduce, list) or not reproduce:
        fail("reproduce must contain at least one command")
    if not all(isinstance(cmd, str) and cmd.strip() for cmd in reproduce):
        fail("every reproduce entry must be a non-empty string")

    score = data.get("score")
    if score is not None and (not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 100):
        fail("score must be null or a number from 0 to 100")

    elapsed = data.get("elapsed_minutes")
    if elapsed is not None and (not isinstance(elapsed, (int, float)) or isinstance(elapsed, bool) or elapsed < 0):
        fail("elapsed_minutes must be null or non-negative")

    sha = data.get("commit_sha")
    if sha is not None and (not isinstance(sha, str) or not SHA40.fullmatch(sha)):
        fail("commit_sha must be null or a lowercase 40-character Git SHA")

    critical = data.get("critical_failures", [])
    if not isinstance(critical, list) or not all(isinstance(x, str) for x in critical):
        fail("critical_failures must be a list of strings")

    if data["status"] in {"portfolio-ready", "externally-verified"}:
        if score is None or score < 80:
            fail("portfolio-ready/external status requires score >= 80")
        if critical:
            fail("portfolio-ready/external status cannot have critical failures")

    warnings: list[str] = []
    if data["evidence_mode"] == "U" and disclosure.get("used"):
        warnings.append("U mode declares AI use; narrow the unaided claim or change evidence_mode")
    if data["status"] == "externally-verified" and not data.get("proctor"):
        warnings.append("externally-verified status should identify the external verifier/proctor")
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()

    try:
        data = json.loads(args.receipt.read_text(encoding="utf-8"))
        warnings = validate(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print("PASS: receipt core invariants satisfied")
    for warning in warnings:
        print(f"WARN: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
