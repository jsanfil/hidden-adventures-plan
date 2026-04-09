# Feature: Map Discovery + Location Search

## Summary

Deliver the real map discovery experience and add location search that can drive both feed and map results.

## Status

- Program status: `In Progress`
- Completion source of truth: this document

## Scope

- real map view in iOS
- shared discovery state between feed and map
- location search input on the main discovery surface
- vague search input such as `Yosemite` or `near Malibu`
- candidate-location results
- selected-location discovery mode with a 25-mile radius
- default current-location discovery mode

## Dependencies

- PostGIS-backed location queries
- approved discovery UX for feed and map coordination

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- location search endpoint or service integration that returns candidate locations
- feed and map query support for current location or selected location
- explicit 25-mile filtering behavior around the selected location

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for location search and filtered discovery
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- Feed and map should stay synchronized when a searched location is selected.
- Current location remains the default until the user explicitly changes scope.
