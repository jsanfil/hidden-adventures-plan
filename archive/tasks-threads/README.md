# Codex Repo Lane Ops

Historical only. These archived lane briefs are preserved for context and must not be used to decide current repo-next work, current thread structure, or program sequencing.

These docs describe the retired repo-lane model that was used before the current repo-autonomous planning rules.

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

Historical server note:

- `thread-2-slice-1-contract-lock.md` and `thread-4-deployment-baseline.md` both targeted `hidden-adventures-server` in the retired model. That old constraint is preserved here for context only.

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
- Slice 2 work should start deliberately and only after the planning lane updates the program docs for any scope or milestone shift
