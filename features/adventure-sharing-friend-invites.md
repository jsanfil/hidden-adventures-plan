# Feature: Adventure Sharing + Friend Invites

## Summary

Make it easy for current users to do two different things well:

- share a specific public adventure with other people
- invite real-world friends to download and start using Hidden Adventures

This feature intentionally separates `Share Adventure` from `Invite Friends`.

`Share Adventure` is a lightweight content-sharing action launched from Adventure Detail.

`Invite Friends` is a dedicated growth flow launched from the signed-in viewer's Profile and optimized for inviting non-users by SMS.

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

- Program status: `Not Started`
- Completion source of truth: this document

## Product Direction

The feature ships as two related but distinct user experiences.

### 1. Invite Friends

`Invite Friends` is a dedicated acquisition flow for inviting non-users into Hidden Adventures.

The entrypoint lives on the signed-in viewer's `Profile`.

The primary send channel in v1 is `SMS`.

The intended UX is:

- the user opens Profile and taps `Invite Friends`
- the app explains why it wants Contacts access
- after permission is granted, the app shows a searchable list of contacts with names and SMS-capable phone numbers
- the user selects one or more recipients
- the app opens the system SMS composer with prefilled invite copy and an app link
- after the user sends or cancels, the app returns to Hidden Adventures with a lightweight completion state

If Contacts permission is denied or restricted, the app should provide a clear fallback path rather than dead-ending the flow.

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
- Contacts permission education and request flow for invites
- searchable contacts list for invite recipient selection
- SMS composer handoff with prefilled invite copy and app link
- public-adventure share action on Adventure Detail
- native iOS share sheet for adventure sharing
- stable link strategy for shared public adventures
- clear unavailable/explanatory state for non-public adventure sharing
- invite copy and lightweight completion states

### Out Of Scope For V1

- pending invite inbox or invite acceptance management
- in-app friend request lifecycle
- referral attribution or reward logic
- contact syncing into Hidden Adventures backend
- using Contacts as the main recipient source for general adventure sharing
- external sharing of `sidekicks` or `private` adventures
- making this feature a Sidekicks-management extension

## UX Notes

### Invite Friends UX Principles

- optimize for getting real-world friends into the app
- make the flow feel intentional and growth-oriented, not like a generic share action
- use Contacts because the product goal requires recognizable people and phone numbers inside the app
- keep SMS sending in the system composer rather than building a custom messaging experience

### Share Adventure UX Principles

- keep adventure sharing fast and native
- do not require Contacts permission for general sharing
- treat the system share sheet as the source of share targets and recipient suggestions
- keep the experience focused on sending a place, not managing an invite relationship

## Dependencies

- stable adventure detail deep link target
- adventure URL strategy for public adventures
- iOS share sheet integration
- iOS Contacts permission and contacts access strategy
- iOS SMS composer strategy

## Public Interface Expectations

- shareable `public` adventure URL/deep-link strategy
- app-side support for contact-backed SMS invite recipient selection
- app-side support for SMS invite copy and composer handoff
- minimal server dependency unless invite/referral tracking becomes a confirmed requirement later

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for any backend support that becomes necessary
- [ ] integrated local happy path validated for invite and share flows
- [ ] manual QA notes recorded

## Notes

- `Invite Friends` and `Share Adventure` may share link infrastructure, but they should remain separate user-facing concepts.
- `Invite Friends` is about app acquisition.
- `Share Adventure` is about content distribution.
- Keep server dependency minimal unless tracking or attribution becomes a concrete requirement.
