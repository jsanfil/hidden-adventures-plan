# Feature: Support, Reporting, And Account Management

## Summary

Add trust, support, and account-management surfaces so the rebuilt app covers the operational user flows that exist in the product feature floor.

## Status

- Program status: `Not Started`
- Completion source of truth: this document

## Scope

- contact support flow
- report content flow
- legal and settings surfaces
- logout polish where needed
- delete-account flow

## Dependencies

- stable authenticated app shell
- content identity and profile identity foundations

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- support request server surface
- content report server surface
- delete-account behavior and audit considerations
- legal and settings navigation support

## QA And Proof

- [ ] v0 screenshots and UX notes linked where applicable
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for support, report, and delete-account behavior
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- Treat support and reporting as shipped product behavior, not as a post-launch afterthought.
