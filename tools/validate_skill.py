#!/usr/bin/env python3
"""Small standalone validator for the repository's Codex skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/rebuild-method.md",
    "scripts/init_rebuild_workspace.py",
    "scripts/validate_rebuild_report.py",
    "assets/contracts/scene_contract.template.json",
    "assets/reports/validation_report.template.json",
]


def validate(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (skill_dir / relative).exists():
            errors.append(f"Missing required file: {relative}")

    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        text = skill_md.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not match:
            errors.append("SKILL.md is missing YAML frontmatter.")
        else:
            frontmatter = match.group(1)
            if "name: blender-reference-rebuild" not in frontmatter:
                errors.append("SKILL.md frontmatter has the wrong name.")
            if "description:" not in frontmatter:
                errors.append("SKILL.md frontmatter is missing description.")
        for phrase in [
            "screen-space contract",
            "world-space contract",
            "blocking_geometry_status",
            "screen_space_status",
            "Blender MCP",
        ]:
            if phrase not in text:
                errors.append(f"SKILL.md missing expected guidance: {phrase}")

    return errors


def main() -> int:
    skill_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "skills/blender-reference-rebuild")
    errors = validate(skill_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Skill is valid: {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

