# Workstream: iOS App

## Goal

Create the new SwiftUI app foundation and deliver the mobile client for each release slice, with the immediate focus on turning the existing Slice 1 shell into a real server-backed flow.

## Scope

- Xcode project bootstrap
- app architecture
- design system implementation
- auth bootstrap
- feed, map, detail, creation, profile, and social flows

## Deliverables

- [x] Xcode project created in repo
- [x] app module structure agreed
- [x] Slice 1 screens and navigation implemented for the native fixture-backed UI flow
- [x] Slice 1 UI test harness documented and checked in
- [ ] real server-backed Slice 1 services
- [ ] real auth/bootstrap wiring

## Dependencies

- product and UX direction
- locked server API contracts for each slice

## Current State

- The native Slice 1 shell exists and is usable for parity work and UI validation.
- The app still relies on fixture-backed services and a fixture-backed viewer identity, so the next milestone is real API integration rather than additional shell invention.
- The `UITEST_START_SCREEN` gallery and walkthrough harness are now part of the required Slice 1 acceptance path and must survive the integration work.

## Source of Truth

- `hidden-adventures-plan` defines scope, flow boundaries, and acceptance criteria.
- `v0-hidden-adventures-ui` is the canonical visual reference for Slice 1 parity work.
- `hidden-adventures-ios` owns native implementation details, test instrumentation, and explicit native behavior overrides.

## Integration Priority

- replace fixture-backed services with real network clients
- wire auth/bootstrap into the app shell
- preserve direct-launch and walkthrough UI test coverage during integration
- keep any temporary fallbacks explicit and documented rather than silent

## v0-to-SwiftUI Workflow

- Pull visual direction and screen composition from `v0-hidden-adventures-ui`.
- If a v0 change implies a product or navigation change, update the plan repo before implementing it natively.
- Implement approved screens in SwiftUI inside `hidden-adventures-ios`.
- Add or update stable `accessibilityIdentifier` coverage for visually critical or interactive elements touched by the change.
- Validate every parity change with `Scripts/run_ui_gallery.sh`.
- Compare generated iOS screenshots against the matching v0 screen or approved screenshot reference before closing the work.

## Testing

- Treat `UITEST_START_SCREEN` launch routing as part of the approved UI debugging and screenshot interface.
- Treat stable `accessibilityIdentifier` coverage as required UI infrastructure, not optional test decoration.
- The required Slice 1 UI suites are:
  - direct-launch gallery for deterministic per-screen screenshots
  - end-to-end walkthrough for navigation and shell safety
- The standard acceptance path for Slice 1 UI changes is:
  - simulator build
  - gallery screenshot run
  - walkthrough run
  - visual comparison against the matching v0 screen or approved screenshot reference
- The standard acceptance path for Slice 1 integration changes is:
  - lock server contracts first
  - replace fixture-backed service usage
  - rerun the UI suites
  - validate the local happy path against the real server

## Done Means

- slice-specific acceptance criteria are met
- app builds locally in Xcode
- Slice 1 is no longer fixture-backed for its core happy path
- linked issue and PR are closed
