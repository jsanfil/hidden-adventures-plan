# Feature: Create Adventure

## Summary

Deliver the first authoring flow so a user can create a new adventure with title, description, category, location, primary media, and visibility.

## Status

- Program status: `Next Up`
- Completion source of truth: this document

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

## Notes

- Keep the fixture-backed authoring path intact after integration.
- Do not invent per-user ACL behavior; creation must use the existing visibility model.
