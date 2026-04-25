#!/usr/bin/env bash

set -euo pipefail

ROOT="/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/hidden-adventures-plan"
BUG_TEMPLATE_SOURCE="$ROOT/templates/github-issue-templates/bug-report.md"
IOS_REPO_ROOT="/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/hidden-adventures-ios"
SERVER_REPO_ROOT="/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/hidden-adventures-server"

REMOTE_REPOS=(
  "jsanfil/hidden-adventures-ios"
  "jsanfil/hidden-adventures-server"
)

TARGET_PATH=".github/ISSUE_TEMPLATE/bug-report.md"
MODE="${1:---remote}"

install_repo_bug_template() {
  local repo_root="$1"
  local target_dir="$repo_root/.github/ISSUE_TEMPLATE"

  mkdir -p "$target_dir"
  cp "$BUG_TEMPLATE_SOURCE" "$target_dir/bug-report.md"
  echo "Installed bug issue template in $repo_root"
}

install_remote_bug_template() {
  local repo="$1"
  local content sha

  content="$(base64 < "$BUG_TEMPLATE_SOURCE" | tr -d '\n')"
  sha="$(gh api "repos/$repo/contents/$TARGET_PATH" --jq '.sha' 2>/dev/null || true)"

  if [[ -n "$sha" ]]; then
    gh api \
      --method PUT \
      -H "Accept: application/vnd.github+json" \
      "repos/$repo/contents/$TARGET_PATH" \
      -f message="Install lightweight bug issue template" \
      -f content="$content" \
      -f sha="$sha" \
      >/dev/null
    echo "Updated remote bug issue template in $repo"
    return
  fi

  gh api \
    --method PUT \
    -H "Accept: application/vnd.github+json" \
    "repos/$repo/contents/$TARGET_PATH" \
    -f message="Install lightweight bug issue template" \
    -f content="$content" \
    >/dev/null
  echo "Created remote bug issue template in $repo"
}

case "$MODE" in
  --remote)
    for repo in "${REMOTE_REPOS[@]}"; do
      install_remote_bug_template "$repo"
    done
    ;;
  --local)
    install_repo_bug_template "$IOS_REPO_ROOT"
    install_repo_bug_template "$SERVER_REPO_ROOT"
    ;;
  *)
    echo "Usage: $0 [--remote|--local]" >&2
    exit 1
    ;;
esac
