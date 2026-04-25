#!/usr/bin/env bash

set -euo pipefail

ROOT="/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/hidden-adventures-plan"
TARGET_DIR="/Users/josephsanfilippo/.codex/skills"

skills=(
  "create-github-bug"
  "triage-github-bugs"
  "execute-github-bug"
)

mkdir -p "$TARGET_DIR"

for skill in "${skills[@]}"; do
  source_path="$ROOT/codex-skills/$skill"
  target_path="$TARGET_DIR/$skill"

  if [[ ! -d "$source_path" ]]; then
    echo "Missing skill directory: $source_path" >&2
    exit 1
  fi

  rm -f "$target_path"
  ln -s "$source_path" "$target_path"
  echo "Linked $skill -> $source_path"
done
