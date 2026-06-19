#!/usr/bin/env python3
"""Validate the layered report shape expected by blender-reference-rebuild."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


STATUS_KEYS = [
    "blocking_geometry_status",
    "screen_space_status",
    "world_geometry_status",
    "perceptual_status",
    "final_status",
]

VALID_STATUSES = {"pass", "fail", "warn", "unknown", "not_applicable"}

REQUIRED_SECTIONS = [
    "blocking_geometry",
    "screen_space",
    "world_geometry",
    "perceptual",
    "artifacts",
]


def validate_report(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"Could not read JSON: {exc}"]

    if not isinstance(data, dict):
        return ["Report root must be a JSON object."]

    for key in STATUS_KEYS:
        value = data.get(key)
        if value is None:
            errors.append(f"Missing status key: {key}")
        elif value not in VALID_STATUSES:
            errors.append(
                f"{key} must be one of {sorted(VALID_STATUSES)}, got {value!r}"
            )

    for section in REQUIRED_SECTIONS:
        if section not in data:
            errors.append(f"Missing section: {section}")
        elif not isinstance(data[section], dict):
            errors.append(f"Section must be an object: {section}")

    artifacts = data.get("artifacts", {})
    if isinstance(artifacts, dict):
        useful_artifacts = [
            value for value in artifacts.values() if isinstance(value, str) and value
        ]
        if data.get("final_status") == "pass" and len(useful_artifacts) < 4:
            errors.append(
                "final_status is pass, but fewer than four artifact paths are recorded."
            )

    screen_space = data.get("screen_space", {})
    if isinstance(screen_space, dict) and data.get("screen_space_status") == "pass":
        if not screen_space.get("objects"):
            errors.append("screen_space_status is pass, but no object evidence exists.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", help="Path to validation_report.json")
    args = parser.parse_args()
    report = Path(args.report).resolve()
    errors = validate_report(report)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Report is valid: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

