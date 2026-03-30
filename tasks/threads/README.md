# Codex Repo Lane Ops

Use these docs to run Codex work by repo, not by worktree.

## Current Operating Model

- Keep one planning and status thread in `hidden-adventures-plan`.
- Keep one backend or ops thread in `hidden-adventures-server`.
- Keep one app thread in `hidden-adventures-ios`.
- Open `hidden-adventures-api-tests` only when the manual troubleshooting assets need to change.
- Open `v0-hidden-adventures-ui` only when Slice 2 UX reference work is active.

## Playbooks By Repo

- `thread-1-program-control.md`: plan repo control tower and status sync
- `thread-2-slice-1-contract-lock.md`: server contract maintenance on the locked Slice 1 surface
- `thread-3-ios-real-integration.md`: iOS live-runtime acceptance and fallback cleanup
- `thread-4-deployment-baseline.md`: server deployment and staging execution lane
- `thread-5-slice-2-ux.md`: Slice 2 UX and screen-map definition work in `v0-hidden-adventures-ui`

Server note:

- `thread-2-slice-1-contract-lock.md` and `thread-4-deployment-baseline.md` both target `hidden-adventures-server`. Do not run them as separate active implementation threads at the same time. Reuse the one active server thread and switch phase focus as needed.

## How To Use In Codex App

For each repo lane:

1. open or reuse the Codex App thread that already owns that repo
2. switch to the owning repo as the working directory
3. stay on the repo's `main` branch unless there is a repo-specific reason not to
4. paste the `Startup Prompt` section from the lane brief
5. keep the work inside the lane's `Allowed Scope`
6. require the lane to end each cycle with the `Handoff Format`

## Global Rules

- the planning lane is the only lane that should update program-wide status docs by default
- the iOS lane should not infer contracts the server lane has not already locked
- the server lane should treat Vitest as the official verification path
- Postman is a manual troubleshooting companion and must stay current only when the live API changes
- Slice 2 work stays definition-only until Slice 1 live local acceptance is closed
