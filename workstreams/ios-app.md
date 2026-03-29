# Workstream: iOS App

## Goal

Create the new SwiftUI app foundation and deliver the mobile client for each release slice.

## Scope

- Xcode project bootstrap
- app architecture
- design system implementation
- auth bootstrap
- feed, map, detail, creation, profile, and social flows

## Deliverables

- [x] Xcode project created in repo
- [x] app module structure agreed
- [x] slice 1 screens and navigation implemented for the native mock-backed UI flow
- [ ] test strategy documented (in progress)

## Dependencies

- product and UX direction
- server API contracts for each slice

## Source of Truth

- `hidden-adventures-plan` defines scope, flow boundaries, and acceptance criteria.
- `v0-hidden-adventures-ui` is the canonical visual reference for slice-1 parity work.
- `hidden-adventures-ios` owns native implementation details, test instrumentation, and explicit native behavior overrides.

## v0-to-SwiftUI Workflow

- Pull visual direction and screen composition from `v0-hidden-adventures-ui`.
- If a v0 change implies a product or navigation change, update the plan repo before implementing it natively.
- Implement approved screens in SwiftUI inside `hidden-adventures-ios`.
- Add or update stable `accessibilityIdentifier` coverage for visually critical or interactive elements touched by the change.
- Validate every parity change with `Scripts/run_ui_gallery.sh`.
- Compare generated iOS screenshots against the matching v0 screen or approved screenshot reference before closing the work.

## Parity Bug Process

- Track one UI parity bug at a time.
- Do not move to the next bug until the current one has code, screenshot retest, and regression coverage completed.
- Every visual fix must strengthen the UI harness with assertions, screenshots, or both.

## Native Behavior Override

- v0 is the visual reference for slice 1, but not a mandate to copy web-only behavior.
- Prefer cleaner native SwiftUI behavior when layout safety, accessibility, or platform ergonomics require it.
- Record any intentional divergence explicitly in this workstream or the linked task instead of making it implicitly.

## Testing

- Treat `UITEST_START_SCREEN` launch routing as part of the approved UI debugging and screenshot interface.
- Treat stable `accessibilityIdentifier` coverage as required UI infrastructure, not optional test decoration.
- The required slice-1 UI suites are:
  - direct-launch gallery for deterministic per-screen screenshots
  - end-to-end walkthrough for navigation and shell safety
- The standard acceptance path for slice-1 UI changes is:
  - simulator build
  - gallery screenshot run
  - walkthrough run
  - visual comparison against the matching v0 screen or approved screenshot reference
- `Scripts/run_ui_gallery.sh`, the generated screenshot folders, and the `.xcresult` bundle are the standard artifacts for slice-1 UI review.

## Done Means

- slice-specific acceptance criteria are met
- app builds locally in Xcode
- linked issue and PR are closed
