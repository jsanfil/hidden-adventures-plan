#!/usr/bin/env bash

set -euo pipefail

OWNER="jsanfil"
PROJECT_TITLE="Hidden Adventures Bug Workflow"
IOS_REPO="jsanfil/hidden-adventures-ios"
SERVER_REPO="jsanfil/hidden-adventures-server"

usage() {
  cat <<'EOF'
Usage: ./scripts/setup_github_bug_project.sh [--owner <login>] [--title <project-title>]

Creates or reuses the shared Hidden Adventures bug workflow project, links the
iOS and server repos, and ensures the custom workflow fields exist.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --owner)
      OWNER="${2:?missing owner value}"
      shift 2
      ;;
    --title)
      PROJECT_TITLE="${2:?missing title value}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

project_number="$(
  gh project list --owner "$OWNER" --format json \
    --jq ".projects[] | select(.title == \"$PROJECT_TITLE\") | .number" \
    | head -n 1
)"

if [[ -z "$project_number" ]]; then
  project_number="$(
    gh project create --owner "$OWNER" --title "$PROJECT_TITLE" --format json \
      --jq '.number'
  )"
  echo "Created project #$project_number: $PROJECT_TITLE"
else
  echo "Reusing project #$project_number: $PROJECT_TITLE"
fi

gh project link "$project_number" --owner "$OWNER" --repo "$IOS_REPO"
gh project link "$project_number" --owner "$OWNER" --repo "$SERVER_REPO"

ensure_field() {
  local field_name="$1"
  local data_type="$2"
  local options="${3:-}"
  local existing

  existing="$(
    gh project field-list "$project_number" --owner "$OWNER" --format json \
      --jq ".fields[] | select(.name == \"$field_name\") | .id" \
      | head -n 1
  )"

  if [[ -n "$existing" ]]; then
    echo "Field already exists: $field_name"
    return
  fi

  if [[ -n "$options" ]]; then
    gh project field-create "$project_number" \
      --owner "$OWNER" \
      --name "$field_name" \
      --data-type "$data_type" \
      --single-select-options "$options" \
      >/dev/null
  else
    gh project field-create "$project_number" \
      --owner "$OWNER" \
      --name "$field_name" \
      --data-type "$data_type" \
      >/dev/null
  fi

  echo "Created field: $field_name"
}

ensure_field "Priority" "SINGLE_SELECT" "P0,P1,P2"
ensure_field "Area" "TEXT"
ensure_field "Needs Human Decision" "SINGLE_SELECT" "No,Yes"

gh project view "$project_number" --owner "$OWNER" --format json \
  --jq '"Project ready: " + .title + " -> " + .url'
