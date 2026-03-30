# Thread 2: Slice 1 Contract Maintenance

## Owning Repo

- `hidden-adventures-server`

## Mission

Hold the implemented Slice 1 server surface steady so the iOS lane can consume it without guessing. Treat Postman updates as a separate on-demand follow-up only when the manual troubleshooting assets truly need to move.

## Allowed Scope

- server contract docs
- request and response documentation
- additive server refinements that make the implemented endpoints consumable
- local acceptance support that does not expand Slice 1 scope

## Blocked Scope

- broad server feature expansion for Slice 2
- iOS UI work
- using Postman as the acceptance system
- reintroducing `viewerHandle` to the public contract
- direct plan milestone edits; hand facts back to the planning lane instead

## Inputs

- current Fastify routes and Vitest coverage
- published migration-backed local dataset
- Slice 1 release doc

## Deliverables

- locked Slice 1 contract notes
- server gap list for the iOS lane
- any contract-safe acceptance fixes needed for local verification

## Required Checks

- `npm test`
- `npm run check`
- confirm read routes reject `viewerHandle`
- keep business routes bearer-auth only

## Startup Prompt

You are the server contract lane for the Hidden Adventures rebuild. Work only in `hidden-adventures-server` on `main`. Hold the current Slice 1 contract steady from the implemented server routes and tests. Use Vitest as the authoritative server verification suite. Do not treat Postman as formal acceptance, and do not invent new Slice 2 surface area. Produce a handoff that tells the iOS and planning lanes exactly what is stable, what auth is required, and what is still missing. If the manual troubleshooting assets need updates, call that out so a separate `hidden-adventures-api-tests` cycle can pick it up.

## Handoff Format

- what changed
- what is now stable
- what another repo may rely on
- what remains unresolved
