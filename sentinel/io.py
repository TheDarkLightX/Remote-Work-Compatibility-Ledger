"""Strict JSON/JSONL parsing, hashing, and atomic output helpers."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import JsonlParseError


@dataclass(frozen=True)
class LoadedJsonl:
    records: list[dict[str, Any]]
    sha256: str


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-standard numeric constant {value!r} is not allowed")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def strict_json_loads(text: str) -> Any:
    """Parse standards-compliant JSON while rejecting duplicate object keys."""

    return json.loads(
        text,
        object_pairs_hook=_unique_object,
        parse_constant=_reject_constant,
    )


def load_jsonl(path: Path, label: str) -> LoadedJsonl:
    """Load non-empty, object-only JSONL with precise failure locations."""

    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise JsonlParseError(f"{label}: cannot read {path}: {exc}") from exc

    if not raw:
        raise JsonlParseError(f"{label}: {path} is empty")

    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise JsonlParseError(
            f"{label}: {path} is not valid UTF-8 at byte {exc.start}"
        ) from exc

    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            raise JsonlParseError(
                f"{label}: {path}:{line_number}: blank JSONL lines are not allowed"
            )
        try:
            value = strict_json_loads(line)
        except (json.JSONDecodeError, ValueError) as exc:
            location = ""
            if isinstance(exc, json.JSONDecodeError):
                location = f" column {exc.colno}"
            raise JsonlParseError(
                f"{label}: {path}:{line_number}:{location} {exc}"
            ) from exc
        if not isinstance(value, dict):
            raise JsonlParseError(
                f"{label}: {path}:{line_number}: each JSONL record must be an object"
            )
        records.append(value)

    if not records:
        raise JsonlParseError(f"{label}: {path} contains no records")

    return LoadedJsonl(records=records, sha256=hashlib.sha256(raw).hexdigest())


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def stable_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def atomic_write_text(path: Path, content: str) -> None:
    """Replace a UTF-8 text file only after the full content is durable."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise
