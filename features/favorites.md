# Feature: Favorites

## Summary

Add save and unsave capability, show favorite state consistently across discovery, detail, and profile surfaces, and own the remaining favorites-on-profile scope that was previously grouped under `Profile Collections`.

## Status

- Program status: `Not Started`
- Completion source of truth: this document

## Scope

- favorite toggle on feed cards where appropriate
- favorite toggle on adventure detail
- favorite state hydration in discovery, detail, and profile reads
- current-user favorites collection browsing on profile surfaces
- other-user visible favorites collections where product policy permits in v1
- favorites collection empty states and collection navigation on profile surfaces

## Dependencies

- stable authored-profile browsing already shipped on current profile surfaces
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
- profile favorites collection read support, either via dedicated endpoints or expanded profile responses

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for favorite mutation and read state
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- Favorite state should be visible without requiring the client to infer it from separate ad hoc calls.
- Authored-adventure profile browsing is already shipped and should remain unchanged while this feature adds saved-state behavior and favorites collections.
