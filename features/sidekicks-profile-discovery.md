# Feature: Sidekicks + Profile Discovery

## Summary

Make selective sharing meaningful by adding searchable profile discovery and sidekick state transitions early in the roadmap.

## Status

- Program status: `In Progress`
- Completion source of truth: this document

## Scope

- searchable profile discovery
- profile search results UI
- sidekick request flow
- accept and remove sidekick flow
- relationship state display
- sidekick-aware profile browsing and visibility behavior

## Dependencies

- accepted visibility model based on sidekick state
- stable profile lookup foundation

## Delivery Gates

- [x] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- profile search server surface
- sidekick state transition endpoints
- sidekick-aware profile and adventure reads
- policy enforcement for `sidekicks` visibility, currently stored as `connections`

## QA And Proof

- [x] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for sidekick transitions and policy checks
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Current Progress

- The accepted v0 references now include `docs/ux-specs/ProfileSidekicksDesign.md` plus the full `docs/screenshots/ProfileSidekicks*.png` screenshot set in `v0-hidden-adventures-ui`.
- `hidden-adventures-ios` now has a fixture-backed profile-tab implementation for the first mock slice:
  - hard-coded stats row on profile
  - sidekicks preview card and navigation entry point
  - client-only `SidekicksView` with local search, segmented tabs, add flow, and remove confirm/cancel flow
- Focused iOS UI coverage now exercises the profile-sidekicks entry point and sidekicks interactions through `ProfileScreenUITests`.

## Notes

- This feature is prioritized because sharing with a trusted friend group is core product value.
- Do not reintroduce legacy ACL mutation behavior.
