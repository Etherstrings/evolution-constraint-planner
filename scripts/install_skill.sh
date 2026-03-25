#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CODEX_ROOT="${CODEX_HOME:-$HOME/.codex}"
SKILL_DEST="$CODEX_ROOT/skills/evolution-constraint-planner"

mkdir -p "$CODEX_ROOT/skills"
rm -rf "$SKILL_DEST"
cp -R "$ROOT_DIR" "$SKILL_DEST"
rm -rf "$SKILL_DEST/.git"

echo "Installed evolution-constraint-planner to $SKILL_DEST"
echo "Skill entrypoint: $SKILL_DEST/SKILL.md"
