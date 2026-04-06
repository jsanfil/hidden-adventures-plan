# Feature: Comments

## Summary

Add visible comment threads and comment creation on adventure detail while preserving visibility and author identity rules.

## Status

- Program status: `Not Started`
- Completion source of truth: this document

## Scope

- comment list on adventure detail
- comment composer
- empty, loading, and error states
- comment author identity display
- visibility-aware comment read and write behavior

## Dependencies

- stable adventure detail surface
- viewer identity and profile data

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- comment list read support
- comment create endpoint
- visibility enforcement for both reads and writes

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for comment reads and writes
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- Comment presentation should use current profile state rather than denormalized snapshots where possible.
