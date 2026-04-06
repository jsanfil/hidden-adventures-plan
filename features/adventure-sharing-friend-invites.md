# Feature: Adventure Sharing + Friend Invites

## Summary

Make it easy to share individual adventures externally and invite friends into the app through text or social sharing flows.

## Status

- Program status: `Not Started`
- Completion source of truth: this document

## Scope

- shareable links for specific adventures
- text and social share actions
- contacts-based friend invite UX
- app invite send flow by text
- invite copy and success states

## Dependencies

- stable adventure detail deep link target
- iOS share sheet and contacts permissions strategy

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- shareable adventure URL strategy
- optional server support for invite or referral tracking if needed
- client capability for contacts access and text-share behavior

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for any new share or invite backend support
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- Keep server dependency minimal unless tracking or referral attribution becomes a concrete requirement.
