---
name: triage-github-bugs
description: Use when reviewing Hidden Adventures bug issues across the iOS and server repos to normalize labels, priority, repo ownership, and cross-repo coordination before implementation starts.
---

# Triage GitHub Bugs

Use this skill to turn a loose bug queue into a clean worker-ready backlog.

## Goal

Normalize bug issues so execution agents can safely claim one issue at a time without guessing about ownership or status.

## Standard Labels

Treat labels as the canonical workflow state:

- `type:bug`
- `status:triage`
- `status:ready`
- `status:in-progress`
- `status:blocked`
- `status:ready-for-review`
- `status:verified`
- `prio:p0`
- `prio:p1`
- `prio:p2`

Area labels are repo-specific and optional. Add them only when they improve routing.

## Triage Rules

For each issue:

1. Confirm the owning repo is correct.
2. Ensure exactly one active workflow status label is present.
3. Ensure exactly one priority label is present.
4. Add `type:bug` if missing.
5. Add an `area:*` label only when confidence is high.
6. Leave assignees alone unless the user explicitly asks otherwise.

## Cross-Repo Bugs

Create a coordination issue only when the bug truly requires both repos.

Preferred shape:

- coordination issue in `jsanfil/hidden-adventures-plan`
- one child issue in `jsanfil/hidden-adventures-ios` if app work is required
- one child issue in `jsanfil/hidden-adventures-server` if backend work is required

Do not create parent or child issues for speculative follow-up work.

Use the issue body `Related Issues` section to link parent and child issues when comment tooling is unavailable.

## Status Guidance

- Use `status:triage` when ownership, severity, or acceptance is still unclear.
- Use `status:ready` when a single worker can pick it up safely.
- Use `status:blocked` when a real dependency or product decision is missing.
- Do not move work to `status:ready-for-review` or `status:verified` during triage.

## Priority Guidance

- `prio:p0` for production breakage, data loss, auth lockout, or release-blocking defects
- `prio:p1` for important bugs that materially damage a core flow
- `prio:p2` for normal bug backlog work and polish fixes

Default to `prio:p2` unless there is clear evidence for escalation.

## GitHub Project Guidance

If the shared project `Hidden Adventures Bug Workflow` is in use, mirror the label state into it when practical.

Use this mapping:

- `status:ready` -> `Status: Todo`
- `status:in-progress` -> `Status: In Progress`
- `status:ready-for-review` or `status:verified` -> `Status: Done`
- `prio:p0` -> `Priority: P0`
- `prio:p1` -> `Priority: P1`
- `prio:p2` -> `Priority: P2`

Do not block triage on project-field updates. Labels remain the source of truth and the issue is still considered properly triaged even if the project mirror is stale.

## Output

When triage is complete, report:

- which issues were normalized
- any status or priority changes
- any parent-child issue links created
- any issues that remain blocked and why
