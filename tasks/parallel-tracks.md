# Parallel Tracks

Use this file to make repo-based Codex execution explicit and to keep cross-repo handoffs small, testable, and reviewable.

## Current Scheduled Feature

- `Create Adventure`
- Detailed tracking doc: `features/create-adventure.md`

## Standard Feature Loop

Every post-Slice-1 feature should move through the same repo-aware progression:

1. feature UX definition in `v0-hidden-adventures-ui`
2. fixture-backed native implementation in `hidden-adventures-ios`
3. required API work in `hidden-adventures-server`
4. real iOS integration and QA without breaking the fixture-preview harness

## Active Repo Lane Matrix

| Lane | Owner Repo | Current Status | Immediate Goal | Handoff Artifact | Gate To Close |
| --- | --- | --- | --- | --- | --- |
| Planning and doc sync | `hidden-adventures-plan` | Active | keep the roadmap, rollup status, and feature docs aligned with verified repo facts | updated roadmap, feature docs, workstream notes | linked docs merged and consistent |
| Backend and ops | `hidden-adventures-server` | Active | maintain the locked Slice 1 server surface, then add only the APIs needed for the active feature | passing server checks, contract notes, deploy artifact status | active feature server gate passes |
| App integration and acceptance | `hidden-adventures-ios` | Active | preserve Slice 1 runtime stability while executing the active feature loop without breaking fixture preview | runtime notes, passing UI harness results, integration findings | active feature iOS gates pass |
| Manual API troubleshooting assets | `hidden-adventures-api-tests` | On demand | keep Postman troubleshooting requests aligned only when the live Slice 1 API changes | updated request collections and environment notes | troubleshooting assets match the current server surface |
| Feature UX definition | `v0-hidden-adventures-ui` | Active for scheduled feature only | define the next feature clearly enough for native implementation and contract planning | approved visual references, screenshots, and screen-map notes | active feature design gate passes |

## Lane Rules

- Parallelism is allowed across repos, not as multiple active implementation threads in the same repo.
- Each active lane should work on the owning repo's `main` branch unless there is a repo-specific reason to do otherwise.
- `hidden-adventures-plan` is the only repo that should declare milestone status and cross-repo truth.
- Slice 1 integration work must consume the locked Slice 1 contract notes, use bearer-auth viewer identity, and must not reintroduce `viewerHandle` assumptions.
- Vitest is the official server verification path. Postman remains a manual troubleshooting companion only.
- Post-Slice-1 work should be scheduled feature by feature rather than opened as a broad implementation slice.
- Only one major product feature should be active in the delivery loop at a time unless the planning lane explicitly schedules overlap.
- Data migration is no longer an active day-to-day lane. Treat it as closed work with cutover-validation follow-up only.
- Staging and production readiness stay outside the feature loop until the core feature inventory is complete, except for the already checked-in deployment baseline follow-up.

## Execution Order

1. Create Adventure
2. Edit Adventure
3. Map Discovery + Location Search
4. Connections + Profile Discovery
5. Profile Collections
6. Favorites
7. Comments
8. Ratings
9. Adventure Sharing + Friend Invites
10. Expanded Authentication
11. Support, Reporting, And Account Management
12. Later operational phase for staging hardening and production readiness

## Standard Handoff Notes

Every lane handoff should answer:

- what changed
- what is now stable
- what another repo may rely on
- what remains unresolved
