#!/usr/bin/env python3
"""Create the standard workspace for an indoor reference rebuild project."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


STAGES = [
    "reference_annotation",
    "camera_alignment",
    "structure",
    "blocking_geometry",
    "world_geometry",
    "soft_furnishing",
    "materials",
    "lighting",
    "perceptual",
]


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def copy_or_write_json(template: Path, destination: Path, fallback: dict) -> None:
    if destination.exists():
        return
    if template.exists():
        shutil.copy2(template, destination)
        return
    destination.write_text(json.dumps(fallback, indent=2) + "\n", encoding="utf-8")


def create_workspace(target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    (target / "REFERENCE").mkdir(exist_ok=True)
    (target / "LATEST_RESULTS").mkdir(exist_ok=True)
    archive = target / "ITERATION_ARCHIVE"
    archive.mkdir(exist_ok=True)
    for stage in STAGES:
        (archive / stage).mkdir(exist_ok=True)

    root = skill_root()
    copy_or_write_json(
        root / "assets/contracts/scene_contract.template.json",
        target / "REFERENCE/scene_contract.json",
        {"screen_space_contract": {}, "world_space_contract": {}},
    )
    copy_or_write_json(
        root / "assets/reports/validation_report.template.json",
        target / "LATEST_RESULTS/validation_report.json",
        {
            "blocking_geometry_status": "unknown",
            "screen_space_status": "unknown",
            "world_geometry_status": "unknown",
            "perceptual_status": "unknown",
            "final_status": "unknown",
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="Project directory to create or update.")
    args = parser.parse_args()
    create_workspace(Path(args.target).resolve())
    print(f"Created rebuild workspace: {Path(args.target).resolve()}")


if __name__ == "__main__":
    main()

