# Feature: Edit Adventure

## Summary

Allow authors to update an existing adventure's metadata, media, location, category, and visibility using the authoring foundation established by create adventure.

## Status

- Program status: `Not Started`
- Completion source of truth: this document

## Scope

- entry point from authored adventure surfaces
- edit form populated from existing adventure state
- metadata updates
- media replacement or update handling
- location and category updates
- visibility changes

## Dependencies

- create adventure flow completed or stable enough to reuse
- author ownership rules on server routes

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- edit-adventure server surface for owned adventures
- read and write behavior for existing media and visibility values
- validation and authorization rules for author-only mutation

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for edit path
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- Reuse create-adventure patterns instead of creating a second inconsistent authoring model.
- Edit should not silently loosen visibility or ownership rules.
