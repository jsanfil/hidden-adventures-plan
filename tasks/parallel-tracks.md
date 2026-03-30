# Parallel Tracks

Use this file to make repo-based Codex execution explicit and to keep cross-repo handoffs small, testable, and reviewable.

## Active Repo Lane Matrix

| Lane | Owner Repo | Current Status | Immediate Goal | Handoff Artifact | Gate To Close |
| --- | --- | --- | --- | --- | --- |
| Planning and doc sync | `hidden-adventures-plan` | Active | keep the roadmap, release docs, and milestone language aligned with verified repo facts | updated roadmap, slice docs, workstream notes | linked docs merged and consistent |
| Backend and ops | `hidden-adventures-server` | Active | support Slice 1 acceptance closure and execute the first real staging smoke run | passing server checks, staging smoke notes, deploy artifact status | local acceptance support and first staging smoke both recorded |
| App integration and acceptance | `hidden-adventures-ios` | Active | validate the live Slice 1 runtime against the local server without breaking the fixture-preview UI harness | live-runtime notes, fallback inventory, passing UI harness results | local happy path works against the real server |
| Manual API troubleshooting assets | `hidden-adventures-api-tests` | On demand | keep Postman troubleshooting requests aligned only when the live Slice 1 API changes | updated request collections and environment notes | troubleshooting assets match the current server surface |
| Slice 2 UX and spec | `v0-hidden-adventures-ui` | Definition only | refine create, edit, upload, visibility, and expanded screen map without starting implementation | approved visual references and screen maps | Slice 2 can begin later without silently changing Slice 1 contracts |

## Lane Rules

- Parallelism is allowed across repos, not as multiple active implementation threads in the same repo.
- Each active lane should work on the owning repo's `main` branch unless there is a repo-specific reason to do otherwise.
- `hidden-adventures-plan` is the only repo that should declare milestone status and cross-repo truth.
- Slice 1 integration work must consume the locked Slice 1 contract notes, use bearer-auth viewer identity, and must not reintroduce `viewerHandle` assumptions.
- Vitest is the official server verification path. Postman remains a manual troubleshooting companion only.
- Slice 2 work may continue only as UX and spec definition until Slice 1 local live-runtime acceptance is closed.
- Data migration is no longer an active day-to-day lane. Treat it as closed work with cutover-validation follow-up only.

## Stepwise Milestones

1. Documentation reset to the repo-based operating model
2. Slice 1 contract lock held steady on the implemented server surface
3. Slice 1 iOS real integration held steady with the fixture-preview harness preserved
4. Slice 1 end-to-end local acceptance verified against the live local server
5. First real staging smoke execution recorded from the checked-in deployment baseline
6. Slice 2 implementation start after Slice 1 acceptance closure

## Standard Handoff Notes

Every lane handoff should answer:

- what changed
- what is now stable
- what another repo may rely on
- what remains unresolved
