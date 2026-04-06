# Thread 5: Slice 2 Product And UX Incubation

## Owning Repo

- `v0-hidden-adventures-ui`

## Mission

Move Slice 2 definition forward while Slice 1 acceptance closes. Produce implementation-ready create, edit, upload, and visibility UX references without silently rewriting Slice 1 scope or contracts.

## Allowed Scope

- Slice 2 flow definition
- screen-map expansion
- v0 exploration for Slice 2 concepts
- product copy and visibility UX clarification
- handoff notes for the planning lane to fold back into program docs

## Blocked Scope

- changing locked Slice 1 contracts
- changing Slice 1 navigation without routing it back through the planning lane
- iOS implementation work for Slice 2
- backend contract invention beyond what is needed to express product intent

## Inputs

- current Slice 1 route map
- visibility-model decision
- current v0 visual language
- [workstreams/v0-screen-porting-workflow.md](../../workstreams/v0-screen-porting-workflow.md) for the standard artifact and handoff pattern between v0, plan, and iOS

## Deliverables

- implementation-ready Slice 2 flow notes
- expanded screen map
- approved visual direction for create, edit, upload, and visibility

## Required Checks

- Slice 2 definitions do not contradict the current visibility model
- Slice 2 work is clearly marked definition-only until Slice 1 closes
- any required contract additions are called out explicitly rather than assumed

## Startup Prompt

You are the Slice 2 UX lane for the Hidden Adventures rebuild. Work only in `v0-hidden-adventures-ui` on `main`. Define Slice 2 create, edit, upload, and visibility UX clearly enough for later implementation. Do not silently change Slice 1 scope, contracts, or navigation. Keep the work definition-first and hand back clean notes that the planning, backend, and iOS repos can consume later.

## Handoff Format

- what changed
- what is now stable
- what another repo may rely on
- what remains unresolved
