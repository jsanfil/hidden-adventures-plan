# Feature: Connections + Profile Discovery

## Summary

Make selective sharing meaningful by adding searchable profile discovery and connection state transitions early in the roadmap.

## Status

- Program status: `Not Started`
- Completion source of truth: this document

## Scope

- searchable profile discovery
- profile search results UI
- connection request flow
- accept and remove connection flow
- relationship state display
- connection-aware profile browsing and visibility behavior

## Dependencies

- accepted visibility model based on connection state
- stable profile lookup foundation

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- profile search server surface
- connection state transition endpoints
- connection-aware profile and adventure reads
- policy enforcement for `connections` visibility

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for connection transitions and policy checks
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- This feature is prioritized because sharing with a trusted friend group is core product value.
- Do not reintroduce legacy ACL mutation behavior.
