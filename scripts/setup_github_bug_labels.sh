#!/usr/bin/env bash

set -euo pipefail

repos=(
  "jsanfil/hidden-adventures-ios"
  "jsanfil/hidden-adventures-server"
)

create_label() {
  local repo="$1"
  local name="$2"
  local color="$3"
  local description="$4"

  gh label create "$name" \
    --repo "$repo" \
    --color "$color" \
    --description "$description" \
    --force
}

for repo in "${repos[@]}"; do
  create_label "$repo" "type:bug" "d73a4a" "Bug work item"

  create_label "$repo" "status:triage" "f9d0c4" "Needs initial ownership or severity review"
  create_label "$repo" "status:ready" "0e8a16" "Ready for an agent to claim"
  create_label "$repo" "status:in-progress" "fbca04" "Actively being implemented"
  create_label "$repo" "status:blocked" "b60205" "Blocked by dependency or decision"
  create_label "$repo" "status:ready-for-review" "1d76db" "Implementation and validation are complete"
  create_label "$repo" "status:verified" "5319e7" "Human-verified after review or merge"

  create_label "$repo" "prio:p0" "b60205" "Release-blocking or production-critical defect"
  create_label "$repo" "prio:p1" "d93f0b" "Important bug affecting a core flow"
  create_label "$repo" "prio:p2" "fbca04" "Normal bug backlog priority"

  create_label "$repo" "needs:ios" "0052cc" "Requires iOS repo work"
  create_label "$repo" "needs:server" "0052cc" "Requires server repo work"
  create_label "$repo" "needs:cross-repo" "5319e7" "Requires coordination across repos"
done

echo "Base bug labels synced for iOS and server repos."
