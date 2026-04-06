# Feature: Favorites

## Summary

Add save and unsave capability and show favorite state consistently across discovery, detail, and profile surfaces.

## Status

- Program status: `Not Started`
- Completion source of truth: this document

## Scope

- favorite toggle on feed cards where appropriate
- favorite toggle on adventure detail
- favorites collection support on profile surfaces
- favorite state hydration in discovery and detail reads

## Dependencies

- profile collections planning
- stable adventure identity and viewer auth context

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- favorite create and delete endpoints
- favorite-state inclusion in relevant read models

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for favorite mutation and read state
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- Favorite state should be visible without requiring the client to infer it from separate ad hoc calls.
