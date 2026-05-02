# Feature: Ratings

## Summary

Allow users to rate adventures and display rating aggregates consistently on the surfaces that expose rating.

## Status

- Program status: `Done`
- Completion source of truth: this document

## Scope

- rating control on adventure detail
- current-user rating state
- displayed aggregate rating and count
- rating updates where the same user changes a prior rating

## Dependencies

- stable detail surface
- server-side aggregate or derived rating strategy

## Delivery Gates

- [x] Design accepted
- [x] Mock iOS accepted
- [x] Server accepted
- [x] Integrated iOS accepted
- [x] QA accepted

## Public Interface Expectations

- rating create or upsert endpoint
- rating aggregate inclusion in read models where needed

## QA And Proof

- [x] v0 screenshots and UX notes linked
- [x] SwiftUI gallery coverage updated
- [x] server tests added for rating mutation and aggregate behavior
- [x] integrated local happy path validated
- [x] manual QA notes recorded

## Notes

- Ratings should follow the rebuilt relational model rather than the legacy inline aggregate mutation approach.
- `hidden-adventures-server` now exposes `POST /api/adventures/:id/rating` and `DELETE /api/adventures/:id/rating`, and `GET /api/adventures/:id` now includes nullable `viewerRating` for the authenticated viewer only.
- Server aggregate refresh preserves imported legacy rating baseline through `public.adventure_stats` while layering rebuild-era per-user rows from `public.adventure_ratings` on top.
- `hidden-adventures-ios` now ships integrated rating create, update, and clear flows on adventure detail, updates feed-visible aggregate state when returning from detail, and preserves deterministic fixture-preview coverage for screenshots and UI automation.

## Proof Links

- `v0-hidden-adventures-ui`: `docs/ux-specs/AdventureDetailDesign.md`
- `hidden-adventures-server`: `docs/contract.md`
- `hidden-adventures-server`: `tests/adventures.routes.test.ts`
- `hidden-adventures-server`: `tests/adventures.repository.test.ts`
- `hidden-adventures-server`: `tests/app.test.ts`
- `hidden-adventures-ios`: `Tests/AdventureServiceTests.swift`
- `hidden-adventures-ios`: `UITests/Screens/DetailScreenUITests.swift`
- `hidden-adventures-ios`: `UITests/Screens/ExploreFeedScreenUITests.swift`
- `hidden-adventures-ios`: `UITests/Regression/ScreenGalleryRegressionUITests.swift`
- `hidden-adventures-ios`: `Docs/manual-qa-results.md`
- Verification: `npm test -- tests/adventures.repository.test.ts tests/adventures.routes.test.ts tests/app.test.ts`
- Verification: `npm test`
- Verification: `npm run check`
- Verification: `xcodebuild -project HiddenAdventures.xcodeproj -scheme HiddenAdventures-LocalAutomation -destination 'platform=iOS Simulator,name=iPhone 16' -only-testing:HiddenAdventuresTests/AdventureServiceTests test`
- Verification: `xcodebuild -project HiddenAdventures.xcodeproj -scheme HiddenAdventures-LocalAutomation -destination 'platform=iOS Simulator,name=iPhone 16' -only-testing:HiddenAdventuresUITests/DetailScreenUITests/testDetail_ratingCanBeCreatedUpdatedAndCleared test`
- Verification: `xcodebuild -project HiddenAdventures.xcodeproj -scheme HiddenAdventures-LocalAutomation -destination 'platform=iOS Simulator,name=iPhone 16' -only-testing:HiddenAdventuresUITests/ExploreFeedScreenUITests/testFeedRatingUpdatesAfterReturningFromDetail test`
- Verification: `./Scripts/run_ui_gallery.sh`

## Manual QA Notes

- 2026-05-01: local manual QA passed for ratings, including add, update, and delete on adventure detail plus feed aggregate sync after returning from detail.
