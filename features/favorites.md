# Feature: Favorites

## Summary

Add save and unsave capability, show favorite state consistently across discovery, detail, and profile surfaces, and own the remaining favorites-on-profile scope that was previously grouped under `Profile Collections`.

## Status

- Program status: `Done`
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

- [x] Design accepted
- [x] Mock iOS accepted
- [x] Server accepted
- [x] Integrated iOS accepted
- [x] QA accepted

## Public Interface Expectations

- favorite create and delete endpoints
- favorite-state inclusion in relevant read models
- profile favorites collection read support, either via dedicated endpoints or expanded profile responses

## QA And Proof

- [x] v0 screenshots and UX notes linked
- [x] SwiftUI gallery coverage updated
- [x] server tests added for favorite mutation and read state
- [x] integrated local happy path validated
- [x] manual QA notes recorded

## Manual QA Notes

- Completion accepted by direct program handoff on 2026-04-29.
- Handoff states the Favorites feature is complete across save and unsave behavior, saved-state rendering, profile favorites collection surfaces, server support, iOS integration, and QA.

## Proof Links

- Direct Codex handoff from the program owner on 2026-04-29: "Favorites feature is complete."

## Notes

- Favorite state should be visible without requiring the client to infer it from separate ad hoc calls.
- Authored-adventure profile browsing is already shipped and should remain unchanged while this feature adds saved-state behavior and favorites collections.
- Detailed repo artifact links were not supplied during this planning sync; this doc records the accepted completion handoff without inventing additional proof URLs.
