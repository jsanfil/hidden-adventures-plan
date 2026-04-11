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
- [x] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- location search endpoint or service integration that returns candidate locations
- feed and map query support for current location or selected location
- explicit 25-mile filtering behavior around the selected location

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [x] server tests added for location search and filtered discovery
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Proof Links

- `hidden-adventures-server` commit `c54f479` (`Update feed geo contract and canonical docs`) adds geo-scoped feed query support, distance sorting, radius filtering, and scope metadata on `GET /api/feed`.
- `hidden-adventures-server/docs/contract.md` documents the live geo query contract: `latitude`, `longitude`, `radiusMiles`, optional `sort=distance`, geo scope metadata, and `distanceMiles` on scoped results.
- `hidden-adventures-server/tests/adventures.routes.test.ts`, `tests/adventures.repository.test.ts`, and `tests/app.test.ts` cover route validation, repository filtering and ordering, and end-to-end app responses for geo-scoped discovery reads.
- Local verification on 2026-04-10: `npm test -- tests/adventures.routes.test.ts tests/adventures.repository.test.ts tests/app.test.ts` passed with `3` test files and `36` tests green.

## Notes

- Feed and map should stay synchronized when a searched location is selected.
- Current location remains the default until the user explicitly changes scope.
- Server acceptance currently covers geo-scoped feed reads and the live contract for radius-limited discovery. A dedicated candidate-location search endpoint or external geocoding integration is not yet documented as live in the server contract, so design, integrated iOS, and QA gates remain open.
