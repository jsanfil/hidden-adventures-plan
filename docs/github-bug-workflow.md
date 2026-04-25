# GitHub Bug Workflow

This document defines the lightweight GitHub Issues workflow for Hidden Adventures bug work across `hidden-adventures-ios` and `hidden-adventures-server`.

## Core Model

- Day-to-day bugs live in the owning repo:
  - `jsanfil/hidden-adventures-ios`
  - `jsanfil/hidden-adventures-server`
- `hidden-adventures-plan` stays the rollup and coordination repo, not the default bug queue.
- Labels are the canonical machine-owned workflow state.
- A shared GitHub Project may mirror the label state, but bugs are still actionable without it.
- Only a human merges PRs and closes issues.

## Minimal Intake

Bug intake should work from short natural-language prompts plus optional screenshots.

Example:

> Lets fix the avatar placement on the ProfileView. See how it is too far to the right. See screenshot. Make it line up better with the rest of the view.

Default outcome:

- repo: `jsanfil/hidden-adventures-ios`
- labels: `type:bug`, `status:ready`, `prio:p2`
- minimal issue body using [templates/github-issue-templates/bug-report.md](../templates/github-issue-templates/bug-report.md)

Long bug forms are optional follow-up, not required intake.

## Standard Labels

These labels should exist in both the iOS and server repos:

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
- `needs:ios`
- `needs:server`
- `needs:cross-repo`

Area labels remain repo-specific.

Use [scripts/setup_github_bug_labels.sh](../scripts/setup_github_bug_labels.sh) after GitHub CLI auth is healthy.

## Cross-Repo Bugs

Create a coordination issue only when both repos are truly required.

Preferred shape:

1. parent coordination issue in `jsanfil/hidden-adventures-plan`
2. child bug in `jsanfil/hidden-adventures-ios` if app work is needed
3. child bug in `jsanfil/hidden-adventures-server` if backend work is needed

Do not create parent-child structures for single-repo bugs.

## Execution Contract

Execution agents may:

- claim one `status:ready` bug
- create a branch named `codex/bug-<issue-number>-<slug>`
- implement the fix
- add or update tests
- run validation
- update the issue and PR
- move the issue to `status:ready-for-review`

Execution agents may not:

- merge PRs
- close issues
- mark work verified without human sign-off

## Local Skills

The bug workflow is backed by these local skills stored in this repo:

- `codex-skills/create-github-bug`
- `codex-skills/triage-github-bugs`
- `codex-skills/execute-github-bug`

To register them into personal Codex skills, run:

```bash
./scripts/link_codex_bug_skills.sh
```

This creates symlinks in `~/.codex/skills/`.

## Issue Templates

The reusable template sources live in:

- [templates/github-issue-templates/bug-report.md](../templates/github-issue-templates/bug-report.md)
- [templates/github-issue-templates/cross-repo-bug-coordination.md](../templates/github-issue-templates/cross-repo-bug-coordination.md)

The coordination template is already present in this repo at:

- [.github/ISSUE_TEMPLATE/cross-repo-bug-coordination.md](../.github/ISSUE_TEMPLATE/cross-repo-bug-coordination.md)

To install the lightweight bug template into the iOS and server repos on GitHub, run:

```bash
./scripts/install_github_bug_templates.sh
```

To copy the same template into local sibling checkouts instead, run:

```bash
./scripts/install_github_bug_templates.sh --local
```

## GitHub Project

The shared project is now live at:

- [Hidden Adventures Bug Workflow](https://github.com/users/jsanfil/projects/1)

To create or reconcile the shared project from the CLI, run:

```bash
./scripts/setup_github_bug_project.sh
```

Current field shape:

- `Status`
- `Repository` (built-in)
- `Priority`
- `Area`
- `Needs Human Decision`

The project is linked to:

- `jsanfil/hidden-adventures-ios`
- `jsanfil/hidden-adventures-server`

Current label-to-project mapping:

- `status:ready` -> `Status: Todo`
- `status:in-progress` -> `Status: In Progress`
- `status:ready-for-review` or `status:verified` -> `Status: Done`
- `prio:p0` -> `Priority: P0`
- `prio:p1` -> `Priority: P1`
- `prio:p2` -> `Priority: P2`

Issue labels remain authoritative. The project is a helpful mirror and planning surface, not the canonical workflow state.

## Current Limitation

`gh` auth is now healthy for repository and GitHub Project operations in this workspace, so labels, issues, remote issue-template sync, and project setup can all be managed directly from here.

The remaining workflow gap is automation, not access: issue labels are still the source of truth, and project field values are updated manually or by future helper automation rather than being auto-synced by GitHub.
