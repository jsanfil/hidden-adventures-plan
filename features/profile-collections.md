# Feature: Profile Collections

## Summary

This feature is superseded as a standalone delivery unit. Authored-adventure browsing on profile surfaces already shipped with the existing profile implementation, and the remaining favorites-on-profile scope now belongs to `Favorites`.

## Status

- Program status: `Superseded`
- Completion source of truth: this document

## Scope

- shipped authored adventures collection on profile surfaces
- classification of remaining favorites collection work under `Favorites`

## Dependencies

- stable profile foundation
- verified authored-content profile browsing
- `Favorites` feature planning and implementation for any remaining collection work

## Delivery Gates

- [x] Design accepted
- [x] Mock iOS accepted
- [x] Server accepted
- [x] Integrated iOS accepted
- [x] QA accepted

## Public Interface Expectations

- no new standalone public interface remains under this feature
- any future favorites collection interface belongs to `Favorites`

## QA And Proof

- [x] v0 screenshots and UX notes linked
- [x] SwiftUI gallery coverage updated
- [x] server tests added for authored profile reads
- [x] integrated local happy path validated
- [x] manual QA notes recorded

## Notes

- Existing proof for the shipped authored-profile surface lives in the completed profile and discovery feature work across `hidden-adventures-ios` and `hidden-adventures-server`.
- The live profile contract currently exposes authored adventures through `GET /api/profiles/:handle` with `{ profile, adventures, paging }`.
- Favorites collection browsing, favorite-state hydration, and favorite mutation flows should be tracked only under `Favorites`.
