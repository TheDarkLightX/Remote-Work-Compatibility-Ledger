"""Sentinel exception hierarchy."""

from __future__ import annotations


class SentinelError(Exception):
    """Base class for expected, user-facing Sentinel failures."""


class JsonlParseError(SentinelError):
    """A JSONL file could not be decoded without ambiguity."""


class SchemaValidationError(SentinelError):
    """A decoded record violates its declared data contract."""


class DuplicateIDError(SchemaValidationError):
    """An identifier or composite identifier occurs more than once."""


class CoverageError(SchemaValidationError):
    """The input sets do not have exactly the required coverage."""


class AlignmentError(SchemaValidationError):
    """Redundant identifiers or fingerprints do not align."""


class GraderConfigurationError(SchemaValidationError):
    """A grader's expected condition is malformed or contradictory."""
