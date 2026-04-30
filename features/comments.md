# Feature: Comments

## Summary

Add visible comment threads and comment creation on adventure detail while preserving visibility and author identity rules.

## Status

- Program status: `Done`
- Completion source of truth: this document

## Scope

- comment list on adventure detail
- comment composer
- empty, loading, and error states
- comment author identity display
- visibility-aware comment read and write behavior

## Dependencies

- stable adventure detail surface
- viewer identity and profile data

## Delivery Gates

- [x] Design accepted
- [x] Mock iOS accepted
- [x] Server accepted
- [x] Integrated iOS accepted
- [x] QA accepted

## Public Interface Expectations

- comment list read support
- comment create endpoint
- visibility enforcement for both reads and writes

## QA And Proof

- [x] v0 screenshots and UX notes linked
- [x] SwiftUI gallery coverage updated
- [x] server tests added for comment reads and writes
- [x] integrated local happy path validated
- [x] manual QA notes recorded

## Notes

- Comment presentation should use current profile state rather than denormalized snapshots where possible.
- Server support is implemented in `hidden-adventures-server` for `GET /api/adventures/:id/comments` and `POST /api/adventures/:id/comments`, including visibility checks, completed-local-account enforcement for writes, current profile-backed author fields, and `adventure_stats.comment_count` refresh on create.
- `hidden-adventures-ios` now loads, pages, and creates comments directly from the accepted server contract on adventure detail while preserving deterministic fixture-preview behavior for screenshots and UI automation.

## Proof Links

- `v0-hidden-adventures-ui`: `docs/ux-specs/AdventureDetailDesign.md`
- `hidden-adventures-server`: `docs/contract.md`
- `hidden-adventures-server`: `tests/adventures.routes.test.ts`
- `hidden-adventures-server`: `tests/adventures.repository.test.ts`
- `hidden-adventures-ios`: `Tests/AdventureServiceTests.swift`
- `hidden-adventures-ios`: `UITests/Screens/DetailScreenUITests.swift`
- `hidden-adventures-ios`: `UITests/Regression/ScreenGalleryRegressionUITests.swift`
- Verification: `xcodebuild -project HiddenAdventures.xcodeproj -scheme HiddenAdventures-LocalAutomation -destination 'platform=iOS Simulator,name=iPhone 16' -only-testing:HiddenAdventuresTests/AdventureServiceTests test`
- Verification: `xcodebuild -project HiddenAdventures.xcodeproj -scheme HiddenAdventures-LocalAutomation -destination 'platform=iOS Simulator,name=iPhone 16' -only-testing:HiddenAdventuresUITests/DetailScreenUITests test`
- Verification: `./Scripts/run_ui_gallery.sh`
- Manual QA log: `hidden-adventures-ios/Docs/manual-qa-results.md`

## Manual QA Notes

- 2026-04-29: local manual QA passed for the integrated comments flow, including loading existing comments, creating a new comment, paging additional comments, and verifying empty and error states on adventure detail.
