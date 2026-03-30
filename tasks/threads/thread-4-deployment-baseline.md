# Thread 4: Deployment And Staging Baseline

## Owning Repo

- `hidden-adventures-server`

## Mission

Execute and refine the first repeatable deployment, rollback, environment, and staging smoke-test baseline without changing product scope.

## Allowed Scope

- deployment docs
- environment and secrets docs
- image versioning notes
- staging smoke checklist
- rollback checklist
- light repo changes that support deploy clarity
- staging execution notes captured from a real smoke run

## Blocked Scope

- product feature work
- iOS feature work
- changing Slice 1 contracts unless required for deploy correctness and coordinated through the active server lane

## Inputs

- current server runtime shape
- current Docker workflow
- current program deployment workstream

## Deliverables

- deploy checklist
- rollback checklist
- env and secrets notes
- first staging validation path
- first real staging validation record

## Required Checks

- deploy path is understandable without ad hoc server edits
- rollback path is documented
- staging smoke flow references the actual Slice 1 server surface
- capture the image identifier, runtime shape, smoke results, and any rollback friction from the first real run

## Startup Prompt

You are the deployment and staging lane for the Hidden Adventures rebuild. Work only in `hidden-adventures-server` on `main`. Execute and refine the checked-in deployment baseline for the current Slice 1 server surface. Focus on image versioning, environment and secrets documentation, rollout and rollback steps, and the first real staging smoke flow. Do not drift into feature work. Do not run this as a separate active server thread if another `hidden-adventures-server` implementation thread is already in flight; reuse that thread and switch focus instead.

## Handoff Format

- what changed
- what is now stable
- what another repo may rely on
- what remains unresolved
