# Feature: Map Discovery + Location Search

## Summary

Deliver the real map discovery experience and add location search that can drive both feed and map results.

## Status

- Product priority: `2 of 11`
- Program ship status: `Done`
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

- [x] Design accepted
- [x] Mock iOS accepted
- [x] Server accepted
- [x] Integrated iOS accepted
- [x] QA accepted

## Public Interface Expectations

- location search endpoint or service integration that returns candidate locations
- feed and map query support for current location or selected location
- explicit 25-mile filtering behavior around the selected location

## QA And Proof

- [x] v0 screenshots and UX notes linked
- [x] SwiftUI gallery coverage updated
- [x] server tests added for location search and filtered discovery
- [x] integrated local happy path validated
- [x] manual QA notes recorded

## Manual QA Notes

- Accepted iOS handoff on 2026-04-12 confirms the Explore map flow was completed after the MapKit conversion and that both local automation and manual QA were finished for this feature.
- The shipped map experience now uses the native MapKit-backed Explore surface with location search, discovery-place selection, and synchronized map/feed scope handling.

## Proof Links

- v0 UX spec: [MapViewDesign.md](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/ux-specs/MapViewDesign.md)
- v0 screenshots:
  - [MapView1png.png](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/screenshots/MapView1png.png)
  - [MapView2.png](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/screenshots/MapView2.png)
  - [MapView3.png](/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/v0-hidden-adventures-ui/docs/screenshots/MapView3.png)
- `hidden-adventures-ios` commit `e7a7cc2` (`Added real map into MapExplorerView`) moved the Explore map experience onto a real native map surface.
- `hidden-adventures-ios` commits `5bacdee` (`Updated Map View to meet full enhanced UX`), `963a9b6` (`Basic Mapkit functionality working. Some bugs.`), and `f61e67b` (`Added search location behavior to the Home Feed.`) complete the MapKit-backed map UX, location search behavior, and shared discovery-state flow.
- `hidden-adventures-ios/App/Features/Explore/MapExploreView.swift` and `App/Features/Explore/ExploreLocationSearch.swift` contain the accepted MapKit-backed Explore map and location-search implementation.
- `hidden-adventures-ios/UITests/Regression/ScreenGalleryRegressionUITests.swift` includes `testExploreMap_galleryCapturesScreenshot`, which verifies the map search field, filter button, recenter button, map pins, sheet count, and card content in the deterministic gallery harness.
- `hidden-adventures-server` commit `c54f479` (`Update feed geo contract and canonical docs`) adds geo-scoped feed query support, distance sorting, radius filtering, and scope metadata on `GET /api/feed`.
- `hidden-adventures-server/docs/contract.md` documents the live geo query contract: `latitude`, `longitude`, `radiusMiles`, optional `sort=distance`, geo scope metadata, and `distanceMiles` on scoped results.
- `hidden-adventures-server/tests/adventures.routes.test.ts`, `tests/adventures.repository.test.ts`, and `tests/app.test.ts` cover route validation, repository filtering and ordering, and end-to-end app responses for geo-scoped discovery reads.
- Local verification on 2026-04-10: `npm test -- tests/adventures.routes.test.ts tests/adventures.repository.test.ts tests/app.test.ts` passed with `3` test files and `36` tests green.
- Accepted iOS handoff on 2026-04-12 states that the MapView feature is complete, the map has been converted to MapKit, and both automation and manual QA are complete.

## Notes

- Feed and map should stay synchronized when a searched location is selected.
- Current location remains the default until the user explicitly changes scope.
- The completed feature relies on the accepted live geo-scoped feed contract plus the shipped iOS MapKit search and map coordination flow; future server-side search refinements should be tracked as additive follow-up work, not as an open completion gate for this feature.
