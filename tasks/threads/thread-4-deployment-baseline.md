# Thread 4: Deployment And Staging Baseline

## Owning Repo

- `hidden-adventures-server`

## Recommended Branch

- `codex/deploy-baseline`

## Mission

Define the first repeatable deployment, rollback, environment, and staging smoke-test baseline without changing product scope.

## Allowed Scope

- deployment docs
- environment and secrets docs
- image versioning notes
- staging smoke checklist
- rollback checklist
- light repo changes that support deploy clarity

## Blocked Scope

- product feature work
- iOS feature work
- changing Slice 1 contracts unless required for deploy correctness and coordinated with thread 2

## Inputs

- current server runtime shape
- current Docker workflow
- current program deployment workstream

## Deliverables

- deploy checklist
- rollback checklist
- env and secrets notes
- first staging validation path

## Required Checks

- deploy path is understandable without ad hoc server edits
- rollback path is documented
- staging smoke flow references the actual Slice 1 server surface

## Startup Prompt

You are Thread 4 for the Hidden Adventures rebuild. Work only in `hidden-adventures-server` on branch `codex/deploy-baseline`. Define the first repeatable deployment and staging baseline. Focus on image versioning, environment and secrets documentation, rollout and rollback steps, and a simple staging smoke flow for the current Slice 1 server surface. Do not drift into feature work.

## Handoff Format

- deploy artifacts or docs added
- assumptions about hosting and environment
- staging smoke path
- unresolved risks or missing infra details
