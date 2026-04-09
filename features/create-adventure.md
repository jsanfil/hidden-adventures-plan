# Feature: Create Adventure

## Summary

Deliver the first authoring flow so a user can create a new adventure with title, description, category, location, primary media, and visibility.

## Status

- Product priority: `1 of 11`
- Program ship status: `Done`
- Completion source of truth: this document

## Recommended Feature Loop

1. define and accept Create Adventure UX in `v0-hidden-adventures-ui`
2. build and accept the fixture-backed SwiftUI flow in `hidden-adventures-ios`
3. implement the required create-adventure APIs in `hidden-adventures-server`
4. wire the live iOS integration and QA path without breaking the fixture-backed path

This is the recommended ship path for the feature. It does not forbid additive repo-local prework that stays within the guardrails below.

## Scope

- authoring entry point in the app shell
- create form for title and description
- category selection
- location entry and selection
- primary media selection and upload UX
- visibility selection using `private`, `connections`, and `public`

## Dependencies

- approved v0 authoring screens
- current visibility model
- existing media and profile foundations

## Repo Readiness Notes

- `v0-hidden-adventures-ui`
  Should move first for ship-path work by defining the authoring screens and flow clearly enough for native implementation.
- `hidden-adventures-ios`
  Can prepare local form or media-picking groundwork early, but fixture-backed acceptance should follow approved design.
- `hidden-adventures-server`
  Can prepare additive create-adventure contract or persistence work early if assumptions are documented and no accepted contract is broken.
- `hidden-adventures-plan`
  Should keep this doc aligned with current sequencing, assumptions, and any prework that materially affects the feature.
- `hidden-adventures-api-tests`
  Should wait until a live create-adventure server surface exists before adding troubleshooting assets.

## Delivery Gates

- [x] Design accepted
- [x] Mock iOS accepted
- [x] Server accepted
- [x] Integrated iOS accepted
- [x] QA accepted

## Public Interface Expectations

- create-adventure server surface for draft or publish flow
- request shape for metadata, location, visibility, and primary media association
- upload path or media-linking flow that fits the rebuilt media model

## QA And Proof

- [x] v0 screenshots and UX notes linked
- [x] SwiftUI gallery coverage updated
- [x] walkthrough coverage updated where needed
- [x] server tests added for create path
- [x] integrated local happy path validated
- [x] manual QA notes recorded

## Manual QA Notes

- Tested the feature in the iPhone simulator.
- Verified that created adventure data is written to Postgres and S3.

## Proof Links

- v0 UX spec: [AddAdventure.md](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/ux-specs/AddAdventure.md)
- v0 screenshots:
  - [AddAdventure1.png](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/screenhots/AddAdventure1.png)
  - [AddAdventure2.png](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/screenhots/AddAdventure2.png)
  - [AddAdventure3.png](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/screenhots/AddAdventure3.png)
  - [AddAdventure4.png](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/screenhots/AddAdventure4.png)
  - [AddAdventure5.png](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/screenhots/AddAdventure5.png)
  - [AddAdventure6.png](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/screenhots/AddAdventure6.png)
  - [AddAdventure7.png](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/screenhots/AddAdventure7.png)
  - [AddAdventure8.png](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/screenhots/AddAdventure8.png)
  - [AddAdventure9.png](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/screenhots/AddAdventure9.png)
  - [AddAdventure10.png](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/screenhots/AddAdventure10.png)
- Generated gallery screenshots:
  - [create-photos.png](/tmp/hidden_adventures_ui_tests/gallery/create-photos.png)
  - [create-details-empty.png](/tmp/hidden_adventures_ui_tests/gallery/create-details-empty.png)
  - [create-details-location.png](/tmp/hidden_adventures_ui_tests/gallery/create-details-location.png)
  - [create-location-options.png](/tmp/hidden_adventures_ui_tests/gallery/create-location-options.png)
  - [create-location-search-empty.png](/tmp/hidden_adventures_ui_tests/gallery/create-location-search-empty.png)
  - [create-location-search-results.png](/tmp/hidden_adventures_ui_tests/gallery/create-location-search-results.png)
  - [create-location-pin.png](/tmp/hidden_adventures_ui_tests/gallery/create-location-pin.png)
- Walkthrough captures:
  - [04-create-photos.png](/tmp/hidden_adventures_ui_tests/walkthrough/04-create-photos.png)

## Ship-Required Vs Optional Prework

- `Required before this feature can ship`
  Approved UX, accepted fixture-backed iOS flow, accepted server contract and tests, accepted live iOS integration, and QA proof.
- `Optional repo prework that may happen earlier`
  Additive server groundwork, reusable iOS infrastructure, and provisional UX exploration that helps later execution without redefining the ship path for this feature.

## Notes

- Keep the fixture-backed authoring path intact after integration.
- Do not invent per-user ACL behavior; creation must use the existing visibility model.
- Prework in another repo does not mark this feature active, accepted, or complete on its own.
