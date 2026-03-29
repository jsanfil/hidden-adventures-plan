# Thread 2: Slice 1 Contract Lock

## Owning Repo

- `hidden-adventures-server`
- `hidden-adventures-api-tests`
- `hidden-adventures-plan` for contract-note sync only

## Recommended Branch

- `codex/slice1-contract-lock`

## Mission

Lock the implemented Slice 1 server surface so the iOS integration thread can consume it without guessing. Keep the Postman repo current for manual troubleshooting, but use Vitest as the formal server verification path.

## Allowed Scope

- server contract docs
- request and response documentation
- additive server refinements that make the implemented endpoints consumable
- Postman request updates that mirror the live API
- plan-doc sync limited to contract notes and status updates

## Blocked Scope

- broad server feature expansion for Slice 2
- iOS UI work
- using Postman as the acceptance system
- reintroducing `viewerHandle` to the public contract

## Inputs

- current Fastify routes and Vitest coverage
- published migration-backed local dataset
- Slice 1 release doc

## Deliverables

- locked Slice 1 contract notes
- updated Postman requests for manual auth-backed troubleshooting
- server gap list for the iOS integration thread

## Required Checks

- `npm test`
- `npm run check`
- confirm read routes reject `viewerHandle`
- keep Postman definitions aligned with the live API surface

## Startup Prompt

You are Thread 2 for the Hidden Adventures rebuild. Work in `hidden-adventures-server` and `hidden-adventures-api-tests` on branch `codex/slice1-contract-lock`. Lock the current Slice 1 contract from the implemented server routes and tests. Use Vitest as the authoritative server verification suite. Keep the Postman repo current for manual troubleshooting only; do not treat it as formal acceptance. Do not invent new Slice 2 surface area. Produce a clean handoff that tells the iOS thread exactly what is stable, what auth is required, and what is still missing.

## Handoff Format

- stable endpoints and auth requirements
- payload assumptions the iOS thread may rely on
- tests run and results
- any remaining contract gaps or additive server work needed
