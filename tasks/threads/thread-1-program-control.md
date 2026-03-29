# Thread 1: Program Control And Doc Sync

## Owning Repo

- `hidden-adventures-plan`

## Recommended Branch

- `codex/plan-sync`

## Mission

Keep the rebuild plan repo aligned with verified implementation reality across the sibling repos. This thread owns roadmap truth, slice status, thread coordination notes, and acceptance-language cleanup.

## Allowed Scope

- `master-plan.md`
- `tasks/parallel-tracks.md`
- `releases/`
- `workstreams/`
- task and handoff docs

## Blocked Scope

- server code changes
- iOS code changes
- deployment scripts outside doc-only ops notes
- product or contract invention that is not grounded in verified repo facts

## Inputs

- outputs from threads 2 through 5
- merged or verified changes from sibling repos
- acceptance findings from local checks

## Deliverables

- updated program status when facts change
- updated release and workstream docs when milestones move
- clear handoff notes back to the other threads

## Required Checks

- every completed status must map to a merged or verified artifact
- no doc should contradict the current server surface or the current iOS implementation state
- Slice 1-first sequencing remains explicit

## Startup Prompt

You are Thread 1 for the Hidden Adventures rebuild. Work only in `hidden-adventures-plan` on branch `codex/plan-sync`. Your job is to keep roadmap, slice, and workstream docs aligned with verified facts from the sibling repos. Do not invent server contracts or iOS behavior. Treat Vitest as the official server verification path and Postman as a manual troubleshooting companion only. If another thread changes scope, contracts, or milestone status, update the plan docs to match only after you can point to a concrete artifact.

## Handoff Format

- what repo facts changed
- what docs were updated
- what is now safe for other threads to rely on
- any unresolved contradictions or follow-up docs needed
