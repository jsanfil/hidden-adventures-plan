# Feature: Sidekicks + Profile Discovery

## Summary

Make selective sharing meaningful by adding searchable profile discovery and sidekick state transitions early in the roadmap.

## Status

- Program status: `Done`
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
- [x] Mock iOS accepted
- [x] Server accepted
- [x] Integrated iOS accepted
- [x] QA accepted

## Public Interface Expectations

- profile search server surface
- sidekick state transition endpoints
- sidekick-aware profile and adventure reads
- policy enforcement for `sidekicks` visibility, currently stored as `connections`

## QA And Proof

- [x] v0 screenshots and UX notes linked
- [x] SwiftUI gallery coverage updated
- [x] server tests added for sidekick transitions and policy checks
- [x] integrated local happy path validated
- [x] manual QA notes recorded

## Current Progress

- The accepted v0 references now include `docs/ux-specs/ProfileSidekicksDesign.md` plus the full `docs/screenshots/ProfileSidekicks*.png` screenshot set in `v0-hidden-adventures-ui`.
- `hidden-adventures-ios` now ships the profile-tab sidekicks entry point, live sidekicks list and search flows, add/remove sidekick actions, and sidekick profile-card browsing.
- Focused iOS UI coverage exercises the profile-sidekicks entry point and sidekicks interactions through `ProfileScreenUITests`, while the 2026-04-19 manual QA pass in `hidden-adventures-ios/Docs/manual-qa-results.md` records the integrated local happy path as complete.

## Proof Links

- `v0-hidden-adventures-ui/docs/ux-specs/ProfileSidekicksDesign.md`
- `v0-hidden-adventures-ui/docs/screenshots/ProfileSidekicks*.png`
- `hidden-adventures-server/docs/contract.md`
- `hidden-adventures-server/tests/sidekicks.routes.test.ts`
- `hidden-adventures-server/tests/sidekicks.repository.test.ts`
- `hidden-adventures-ios/UITests/Screens/ProfileScreenUITests.swift`
- `hidden-adventures-ios/Docs/manual-qa-results.md`

## Notes

- This feature is prioritized because sharing with a trusted friend group is core product value.
- Do not reintroduce legacy ACL mutation behavior.
