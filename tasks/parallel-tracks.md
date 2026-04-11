# Parallel Tracks

Use this file to make repo-based Codex execution explicit, define what each repo is allowed to do next, and keep parallel thread scopes small, testable, and reviewable.

## Current Scheduled Feature

- `Map Discovery + Location Search`
- Detailed tracking doc: `features/map-discovery-location-search.md`

## How To Use This File

- Use `Current Scheduled Feature` to answer what the program intends to ship first.
- Use `Repo Backlog Rules` to answer what a given repo is allowed to work on next, including preparatory work ahead of the current scheduled feature.
- Use `Current Active Threads` only as a coordination registry for open threads or worktrees. It does not override the program priority order or feature docs.

## Standard Feature Loop

Every post-Slice-1 feature should move through the same repo-aware progression:

1. feature UX definition in `v0-hidden-adventures-ui`
2. fixture-backed native implementation in `hidden-adventures-ios`
3. required API work in `hidden-adventures-server`
4. real iOS integration and QA without breaking the fixture-preview harness

This is the recommended ship path for a feature. It does not forbid additive repo-local groundwork ahead of the current scheduled feature.

## Repo Backlog Rules

| Repo | Primary Role | Allowed Next Work | Not Allowed To Assume | Handoff Artifact |
| --- | --- | --- | --- | --- |
| `hidden-adventures-plan` | planning source of truth | maintain feature order, repo backlog rules, thread registry, and completion criteria; update docs when repo facts or sequencing assumptions change | implementation-thread state as the authority for program status | updated roadmap, feature docs, task and thread notes |
| `v0-hidden-adventures-ui` | design and UX definition | prioritize design for the current scheduled feature; explore later features when clearly marked provisional and non-binding | that provisional design means a later feature is now active or approved to ship | screenshots, UX notes, screen-map references |
| `hidden-adventures-ios` | fixture-backed UI, live integration, and acceptance | build the scheduled feature after design is accepted; prepare reusable app infrastructure or non-binding groundwork for later features when it does not force product decisions; refactor app code when accepted server contracts change and rerun integration and UI regression coverage | unapproved UX, speculative server contracts, or later-feature groundwork as shipped scope | passing UI harness results, runtime notes, integration findings |
| `hidden-adventures-server` | evolving backend contracts and operational follow-up | maintain accepted live contracts, update existing APIs or schema for scheduled and accepted feature work, and document assumptions for any ahead-of-order work | that ahead-of-time implementation changes ship priority, UX decisions, or undocumented live contract changes | passing checks, evergreen contract notes, migration or deploy notes |
| `hidden-adventures-api-tests` | live troubleshooting assets | update Postman only for live server behavior or accepted current contract changes | speculative future APIs that are not live yet | updated troubleshooting requests and environment notes |

## Repo Rules

- Parallelism is allowed across repos and within a repo.
- Multiple active threads or git worktrees in the same repo are allowed when scopes are explicit, narrow, and non-conflicting.
- Each active thread should work on the owning repo's `main` branch unless there is a repo-specific reason to do otherwise.
- `hidden-adventures-plan` is the only repo that should declare milestone status and cross-repo truth.
- Slice 1 integration work must consume the accepted current server contract notes, use bearer-auth viewer identity, and must not reintroduce `viewerHandle` assumptions.
- Vitest-backed regression coverage is the official server verification path and must move with live contract changes. Postman remains a manual troubleshooting companion only.
- Post-Slice-1 product delivery still follows the program feature order even when repos prepare later work in advance.
- Ahead-of-order server work may revise existing APIs when accepted feature work requires it, but the change must be intentional, documented as live behavior, regression-tested, and handed off to iOS when app code is affected.
- Data migration is no longer an active day-to-day lane. Treat it as closed work with cutover-validation follow-up only.
- Staging and production readiness stay outside the feature loop until the core feature inventory is complete, except for the already checked-in deployment baseline follow-up.
- Historical thread docs under `archive/tasks-threads/` are not authoritative for current repo-next decisions.

## Current Active Threads

This section is optional. Record only the active threads or worktrees that benefit from coordination visibility.

| Thread Or Worktree | Repo | Scope | Related Feature | Blocking Status | Notes |
| --- | --- | --- | --- | --- | --- |
| _none recorded_ | - | - | - | - | Add entries as needed using `tasks/thread-template.md`. |

## Execution Order

1. Create Adventure
2. Map Discovery + Location Search
3. Connections + Profile Discovery
4. Profile Collections
5. Favorites
6. Comments
7. Ratings
8. Adventure Sharing + Friend Invites
9. Expanded Authentication
10. Support, Reporting, And Account Management
11. Edit Adventure
12. Later operational phase for staging hardening and production readiness

## Standard Handoff Notes

Every lane handoff should answer:

- what changed
- what is now stable
- what another repo may rely on
- what remains unresolved
