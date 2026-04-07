# Feature: Create Adventure

## Summary

Deliver the first authoring flow so a user can create a new adventure with title, description, category, location, primary media, and visibility.

## Status

- Product priority: `1 of 11`
- Program ship status: `Next Up`
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

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- create-adventure server surface for draft or publish flow
- request shape for metadata, location, visibility, and primary media association
- upload path or media-linking flow that fits the rebuilt media model

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] walkthrough coverage updated where needed
- [ ] server tests added for create path
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Ship-Required Vs Optional Prework

- `Required before this feature can ship`
  Approved UX, accepted fixture-backed iOS flow, accepted server contract and tests, accepted live iOS integration, and QA proof.
- `Optional repo prework that may happen earlier`
  Additive server groundwork, reusable iOS infrastructure, and provisional UX exploration that helps later execution without redefining the ship path for this feature.

## Notes

- Keep the fixture-backed authoring path intact after integration.
- Do not invent per-user ACL behavior; creation must use the existing visibility model.
- Prework in another repo does not mark this feature active, accepted, or complete on its own.
