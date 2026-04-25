---
name: execute-github-bug
description: Use when implementing a Hidden Adventures bug from GitHub Issues and the workflow should claim one ready bug, create the branch, validate the fix, update issue and PR state, and stop before merge or closure.
---

# Execute GitHub Bug

Use this skill to take exactly one bug from `ready` to `ready-for-review` without merging or closing anything.

## Required Workflow

Before code changes:

- Use `superpowers:test-driven-development` for the implementation itself.
- Use `superpowers:systematic-debugging` if the bug cause is not already obvious.

If the bug is in iOS and requires simulator investigation, use the relevant iOS debugging skill after claiming the issue.

## Claiming Rules

Only claim issues that:

- have `type:bug`
- have `status:ready`
- are not already linked to an active branch or PR

Claim the issue by:

1. removing `status:ready`
2. adding `status:in-progress`
3. if the issue is on the shared project, mirror that state to `Status: In Progress`
4. recording the working branch and intended scope in the issue body or a comment

Never claim more than one issue at a time.

## Branch Naming

Create a branch in the owning repo using:

`codex/bug-<issue-number>-<short-slug>`

Examples:

- `codex/bug-142-profile-avatar-alignment`
- `codex/bug-87-feed-radius-filter`

## Execution Flow

1. Read the issue body and linked evidence carefully.
2. Confirm the owning repo and current branch state.
3. Claim the issue.
4. Reproduce or validate the bug before fixing it when feasible.
5. Add or update tests first.
6. Implement the smallest fix that satisfies the issue.
7. Run the relevant repo validation.
8. Open or update a PR linked to the issue.
9. Update the issue with branch, PR, and validation evidence.
10. Remove `status:in-progress` and add `status:ready-for-review`.
11. If the issue is on the shared project, mirror that state to `Status: Done`.

Stop there.

## Issue Update Contract

Prefer updating these sections in the issue body when direct comment creation is unavailable:

- `Execution Notes`
- `Validation`
- `Related PRs`

Include:

- active branch name
- short scope summary
- tests or checks run
- PR link or number when available

## Repo-Specific Validation

In `hidden-adventures-ios`, run the narrowest relevant validation that still proves the fix:

- targeted build
- targeted XCTest or gallery validation
- simulator or screenshot validation when the bug is visual

In `hidden-adventures-server`, run:

- the narrowest relevant Vitest coverage
- any contract or regression checks affected by the change

Do not mark the issue review-ready without concrete validation evidence.

## Blocking Rules

If the issue is underspecified, blocked by another repo, or needs a product decision:

1. remove `status:in-progress`
2. add `status:blocked`
3. if the issue is on the shared project, mirror that state to `Status: Todo` and set `Needs Human Decision` when appropriate
4. record the blocker in the issue body or comment
5. stop instead of guessing

## Hard Stops

Never do any of these as part of this skill:

- merge the PR
- close the issue
- mark the issue verified without explicit human sign-off
- silently expand scope beyond the claimed bug

## Completion Output

When done, report:

- issue number and repo
- branch name
- validation run
- PR status
- any remaining reviewer risk or follow-up
