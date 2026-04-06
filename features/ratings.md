# Feature: Ratings

## Summary

Allow users to rate adventures and display rating aggregates consistently on the surfaces that expose rating.

## Status

- Program status: `Not Started`
- Completion source of truth: this document

## Scope

- rating control on adventure detail
- current-user rating state
- displayed aggregate rating and count
- rating updates where the same user changes a prior rating

## Dependencies

- stable detail surface
- server-side aggregate or derived rating strategy

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- rating create or upsert endpoint
- rating aggregate inclusion in read models where needed

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for rating mutation and aggregate behavior
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- Ratings should follow the rebuilt relational model rather than the legacy inline aggregate mutation approach.
