# Parallel Tracks

Use this file to make independent Codex threads explicit and to keep cross-thread handoffs small, testable, and reviewable.

## Active Thread Matrix

| Thread | Owner Repo(s) | Current Status | Immediate Goal | Handoff Artifact | Gate To Close |
| --- | --- | --- | --- | --- | --- |
| Program control and doc sync | `hidden-adventures-plan` | Active | keep the program docs aligned with verified repo truth | updated roadmap, slice docs, milestone notes | all linked docs merged and consistent |
| Slice 1 contract lock | `hidden-adventures-server`, `hidden-adventures-api-tests`, `hidden-adventures-plan` | Active | document the implemented server surface and authenticated behavior | locked endpoint notes, authenticated Postman assets, integration gap list | iOS thread can consume contracts without inference |
| Slice 1 iOS real integration | `hidden-adventures-ios` | Ready after contract lock | replace fixture-backed services with real auth and network flows | server-backed Slice 1 client flow and updated UI harness notes | local happy path works against real server |
| Deployment and staging baseline | `hidden-adventures-server` | Active | define deploy, rollback, env, and smoke-test path | deployment checklist, rollback checklist, staging notes | first staging validation can be executed repeatably |
| Slice 2 product and UX incubation | `hidden-adventures-plan`, `v0-hidden-adventures-ui` | Active | refine create, edit, upload, visibility, and expanded screen map | implementation-ready Slice 2 spec and approved visual references | Slice 2 can start without changing Slice 1 contracts silently |

## Thread Rules

- Each thread should own one clear deliverable set and one primary repo or repo pair.
- Threads may run in parallel only when the consumer thread can work from a stable handoff artifact rather than verbal assumptions.
- Slice 1 integration work should not start against undocumented contracts.
- Slice 2 product work may continue in parallel, but it must not quietly rewrite Slice 1 flow boundaries or public interfaces.
- Data migration is no longer an active day-to-day thread. Treat it as closed work with cutover-validation follow-up only.

## Stepwise Milestones

1. Documentation reset
2. Slice 1 contract freeze
3. Slice 1 iOS real integration
4. Slice 1 end-to-end local acceptance
5. Deployment and staging baseline
6. Slice 2 execution start

## Standard Handoff Notes

Every thread handoff should answer:

- what changed
- what is now stable
- what the next thread may rely on
- what remains intentionally unresolved
