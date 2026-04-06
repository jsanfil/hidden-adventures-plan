# Feature: Profile Collections

## Summary

Expand profile surfaces so users can browse authored adventures and favorites on profiles where visibility allows.

## Status

- Program status: `Not Started`
- Completion source of truth: this document

## Scope

- current-user profile collections
- authored adventures collection
- favorites collection
- other-user visible collections where policy permits
- collection navigation and empty states

## Dependencies

- stable profile foundation
- favorites and authored-content read patterns
- visibility-aware profile browsing

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- profile collection read endpoints or expanded profile reads
- visibility-aware collection membership behavior

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for collection reads
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- Profile collections should align with the visibility model and not leak hidden adventures.
