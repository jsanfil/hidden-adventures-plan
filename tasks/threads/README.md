# Codex Thread Ops

Use these docs to launch parallel Codex App threads against the current rebuild plan.

## Recommended Launch Order

1. thread-1-program-control.md
2. thread-2-slice-1-contract-lock.md
3. thread-4-deployment-baseline.md
4. thread-5-slice-2-ux.md
5. thread-3-ios-real-integration.md

Launch thread 3 after thread 2 has produced its first contract handoff.

## Recommended Branches

- thread 1: `codex/plan-sync`
- thread 2: `codex/slice1-contract-lock`
- thread 3: `codex/slice1-ios-real-integration`
- thread 4: `codex/deploy-baseline`
- thread 5: `codex/slice2-ux-incubation`

## How To Use In Codex App

For each thread:

1. open a new Codex App thread
2. switch to the owning repo as the working directory
3. create or switch to the recommended branch
4. paste the `Startup Prompt` section from the thread brief
5. keep the thread within its `Allowed Scope`
6. require the thread to end each cycle with the `Handoff Format`

## Global Rules

- thread 1 is the only thread that should update program-wide status docs by default
- thread 2 owns server contract truth for Slice 1
- thread 3 should not infer contracts that thread 2 has not locked
- thread 4 should not change server behavior except for deploy and ops needs
- thread 5 may define Slice 2 behavior, but must not silently change Slice 1 scope or contracts
- Vitest is the official server verification path
- Postman is a manual troubleshooting companion and must stay current, but it is not the acceptance runner
