# Feature: Link Support + Install Routing

## Summary

Finish the remaining link behavior for sharing and invites by implementing stable client and server support for app-open, install, and fallback routing.

## Status

- Program status: `Not Started`
- Completion source of truth: this document

## Scope

- canonical public link strategy for shared adventures and app invites
- server-owned fallback behavior for links opened without the app installed
- iOS universal-link or equivalent installed-app routing for supported shared destinations
- app-side handling for invite and public-adventure links after launch or cold start
- validation that invite and share links land on the correct in-app destination when supported

## Dependencies

- completed `Adventure Sharing + Friend Invites` baseline behavior
- server support for stable public link routing
- iOS associated-domain and app-routing decisions
- a clear fallback destination when the app is not installed

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- canonical public URL structure for adventure-share and app-invite links
- server routes or web fallback behavior for unresolved app links
- client deep-link parsing and destination routing for invite and adventure surfaces
- documented associated-domain or equivalent app-link configuration

## QA And Proof

- [ ] link-behavior UX notes linked
- [ ] server routing behavior verified
- [ ] iOS installed-app open behavior verified
- [ ] no-app fallback behavior verified
- [ ] manual QA notes recorded for invite and public-adventure link journeys

## Notes

- This is a follow-up completion feature, not a rollback of the shipped native share-sheet behavior.
- Keep the already-shipped `Adventure Sharing + Friend Invites` feature marked complete while tracking the deferred link-routing work here.
- Scope should stay focused on link resolution and routing, not broader referral or growth-program mechanics.
