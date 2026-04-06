# Hidden Adventures Plan

This repo is the global source of truth for the Hidden Adventures rebuild.

## Purpose

- own the master plan
- track cross-repo workstreams
- record architectural decisions
- define the remaining feature inventory and execution order
- provide durable task templates and checklists
- preserve historical planning docs in an archive when they are no longer part of the active operating model

## Repos In Program

- `hidden-adventures-plan`
- `hidden-adventures-ios`
- `hidden-adventures-server`

## Operating Rules

- The master roadmap lives in [master-plan.md](./master-plan.md).
- Workstream details live under [workstreams](./workstreams).
- Architectural decisions live under [decisions](./decisions).
- Active feature-family definitions live under [features](./features).
- Historical slice and thread docs live under [archive](./archive).
- Migration notes live under [migration](./migration).
- Use [workstreams/v0-screen-porting-workflow.md](./workstreams/v0-screen-porting-workflow.md) as the repeatable playbook for any remaining screen port from `v0-hidden-adventures-ui` into `hidden-adventures-ios`.
- Active execution should use both Markdown and your issue board.

## Recommended Cadence

- update `master-plan.md` when scope, sequencing, or risk changes
- update workstream docs when a stream is activated or re-scoped
- record decisions as soon as an architecture choice is locked
- close checklist items only when linked repo work is merged and verified
