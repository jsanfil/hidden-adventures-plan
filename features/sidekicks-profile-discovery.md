# Feature: Sidekicks + Profile Discovery

## Summary

Make selective sharing meaningful by adding searchable profile discovery and sidekick state transitions early in the roadmap.

## Status

- Program status: `Not Started`
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

- [ ] Design accepted
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

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for sidekick transitions and policy checks
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- This feature is prioritized because sharing with a trusted friend group is core product value.
- Do not reintroduce legacy ACL mutation behavior.
