"""Shared fixture helpers for Sentinel tests."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from sentinel.io import strict_json_loads


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SUBMISSION_ROOT = REPOSITORY_ROOT / "submissions" / "EVAL-001" / "dana-v1"
EVALS_PATH = SUBMISSION_ROOT / "evals.jsonl"
RESPONSES_PATH = SUBMISSION_ROOT / "responses.jsonl"
GOLD_PATH = SUBMISSION_ROOT / "gold.jsonl"


def read_records(path: Path) -> list[dict[str, Any]]:
    """Read a trusted committed JSONL fixture using the production strict parser."""

    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        value = strict_json_loads(line)
        if not isinstance(value, dict):  # pragma: no cover - fixture corruption guard
            raise AssertionError(f"fixture record in {path} is not an object")
        records.append(value)
    return records


def fixture_records() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    """Return independent mutable copies of all three committed inputs."""

    return copy.deepcopy(
        (read_records(EVALS_PATH), read_records(RESPONSES_PATH), read_records(GOLD_PATH))
    )


def write_records(path: Path, records: list[dict[str, Any]]) -> None:
    """Write deterministic JSONL for temporary integration fixtures."""

    content = "\n".join(
        json.dumps(
            record,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        for record in records
    )
    path.write_text(content + "\n", encoding="utf-8", newline="\n")
