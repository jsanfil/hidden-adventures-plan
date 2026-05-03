# Feature: Adventure Sharing + Friend Invites

## Summary

Make it easy for current users to do two different things well:

- share a specific public adventure with other people
- invite real-world friends to download and start using Hidden Adventures

This feature intentionally separates `Share Adventure` from `Invite Friends`.

`Share Adventure` is a lightweight content-sharing action launched from Adventure Detail.

`Invite Friends` is a dedicated growth flow launched from the signed-in viewer's Profile and optimized for inviting non-users through the native iOS share sheet.

## Motivation

This feature exists primarily to support user growth and lightweight sharing without prematurely turning Hidden Adventures into a full social-invite management system.

The main motivations are:

- help current users bring their real-world friends into the app
- make adventure posts feel naturally shareable
- support familiar iOS-native sharing behavior instead of inventing custom mechanics where they are not needed
- keep v1 server dependency minimal unless referral tracking or attribution becomes a real product requirement later

This feature is not primarily about managing users who are already connected in the app.

Existing `Sidekicks` behavior remains a separate concept for in-app relationships and discovery.

## Status

- Program status: `Completed`
- Completion source of truth: this document

## Product Direction

The feature ships as two related but distinct user experiences.

### 1. Invite Friends

`Invite Friends` is a lightweight acquisition flow for inviting non-users into Hidden Adventures.

The entrypoint lives on the signed-in viewer's `Profile`.

The intended UX is:

- the user opens Profile and taps `Invite Friends`
- the app opens the native iOS share sheet with a prepared app-invite message and link
- recipient suggestions, names, and share destinations are handled by the system, not by Hidden Adventures
- the invite can be sent by Messages, Mail, AirDrop, copy, or any other supported share destination

This shipped version intentionally avoids Contacts permission, app-owned recipient picking, and a custom SMS-composer flow.

### 2. Share Adventure

`Share Adventure` is a lightweight content-sharing action for a specific adventure.

The entrypoint lives on `Adventure Detail`.

The intended UX is:

- the user opens a public adventure
- the user taps `Share`
- the app opens the native iOS share sheet with a prepared share payload
- recipient suggestions, names, and share destinations are handled by the system, not by Hidden Adventures
- if the recipient has the app installed, the shared link should resolve into the app's adventure detail destination
- if the app is not installed, the shared link should still land somewhere stable enough to support future install/open behavior

In v1, `Share Adventure` is only available for `public` adventures.

`sidekicks` and `private` adventures are not externally shareable in v1.

## Scope

### In Scope

- Profile-based `Invite Friends` entrypoint for the signed-in viewer
- native iOS share sheet handoff for app invites
- prefilled app-invite copy and a stable invite URL
- public-adventure share action on Adventure Detail
- native iOS share sheet for adventure sharing
- stable link strategy for shared public adventures
- clear unavailable or explanatory state for non-public adventure sharing

### Out Of Scope For V1

- pending invite inbox or invite acceptance management
- in-app friend request lifecycle
- referral attribution or reward logic
- contact syncing into Hidden Adventures backend
- Contacts permission or app-owned recipient selection for invites
- a custom SMS-composer flow for invites
- external sharing of `sidekicks` or `private` adventures
- making this feature a Sidekicks-management extension

## UX Notes

### Invite Friends UX Principles

- optimize for getting real-world friends into the app
- keep the flow fast and native
- let the iOS share sheet handle recipients and destinations
- avoid Contacts permission and app-owned recipient management for this shipped version

### Share Adventure UX Principles

- keep adventure sharing fast and native
- do not require Contacts permission for general sharing
- treat the system share sheet as the source of share targets and recipient suggestions
- keep the experience focused on sending a place, not managing an invite relationship

## Dependencies

- stable adventure detail deep link target
- adventure URL strategy for public adventures
- stable app-invite URL strategy
- iOS share sheet integration

## Public Interface Expectations

- shareable `public` adventure URL and deep-link strategy
- app-side support for an invite share payload and native share-sheet handoff from Profile
- minimal server dependency unless invite or referral tracking becomes a confirmed requirement later

## Delivery Gates

- [x] Design accepted
- [x] Mock iOS accepted
- [x] Server accepted
- [x] Integrated iOS accepted
- [x] QA accepted

## QA And Proof

- [x] Focused invite-share payload unit tests passing in `hidden-adventures-ios`
- [x] Focused Profile and Detail UI automation passing in `hidden-adventures-ios`
- [x] Local manual QA recorded in `hidden-adventures-ios/Docs/manual-qa-results.md`
- [x] Public-adventure share availability and non-public share explanation verified
- [x] Profile invite entrypoint now verified against the shipped native share-sheet flow

## Proof Links

- `hidden-adventures-ios/Docs/manual-qa-results.md` records local manual QA for the simplified native share-sheet invite flow and adventure sharing checks.
- Focused passing verification in `hidden-adventures-ios`:
  - `HiddenAdventuresTests/InviteSharePayloadTests`
  - `HiddenAdventuresTests/AdventureSharePayloadTests`
  - `HiddenAdventuresUITests/ProfileScreenUITests/testInviteFriends_andShareAdventure_smoke`
  - `HiddenAdventuresUITests/ProfileScreenUITests/testProfile_inviteFriendsButtonIsAvailable`
  - `HiddenAdventuresUITests/DetailScreenUITests/testDetail_publicAdventureKeepsShareEnabled`
  - `HiddenAdventuresUITests/DetailScreenUITests/testDetail_nonPublicAdventureShowsShareExplanation`

## Notes

- `Invite Friends` and `Share Adventure` share the native iOS share-sheet model but remain separate user-facing concepts.
- `Invite Friends` is about app acquisition.
- `Share Adventure` is about content distribution.
- No additional server contract was required for the shipped native invite-share implementation.
- Keep server dependency minimal unless tracking or attribution becomes a concrete requirement.
