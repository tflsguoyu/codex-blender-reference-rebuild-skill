#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
TARGET="$TARGET_ROOT/blender-reference-rebuild"

mkdir -p "$TARGET_ROOT"
rm -rf "$TARGET"
cp -R "$REPO_ROOT/skills/blender-reference-rebuild" "$TARGET"

echo "Installed blender-reference-rebuild to $TARGET"

