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
- [x] real server-backed Slice 1 services
- [x] real auth/bootstrap wiring

## Dependencies

- product and UX direction
- locked server API contracts for each slice

## Current State

- The native Slice 1 shell exists and is usable for parity work and UI validation.
- The default runtime now composes `RemoteAdventureService`, `RemoteProfileService`, and `RemoteAuthService` at the app root.
- Service protocols no longer expose `viewerHandle` request overrides; the app uses server-backed auth/bootstrap state instead.
- Live server mode is the default outside UI tests, and the app now distinguishes `LocalManualQA`, `LocalAutomation`, and `Production` server configurations.
- Fixture preview remains a deliberate runtime mode for screenshots, previews, and deterministic walkthrough captures.
- The current live Slice 1 fallbacks are explicit rather than silent: feed-derived map cards and placeholder media until later route contracts lock.
- The welcome screen now has two intentful entry points into one email-auth mechanism: `Get Started` for onboarding intent and `Sign In` for returning-user intent.
- New users should continue into handle selection and profile setup only after verified auth when bootstrap returns `new_user_needs_handle`.
- Linked legacy users and linked rebuild users should skip onboarding and land directly in Explore/Feed after verified auth.
- The rebuild app should expose no visible username/password path unless live validation reveals a blocker that forces a temporary fallback.
- The `UITEST_START_SCREEN` gallery and walkthrough harness are now part of the required Slice 1 acceptance path and must survive the integration work.
- The next proof points are explicit validation in both local modes:
  - `LocalAutomation` against the `test-core` dataset and deterministic signed test JWT auth
  - `LocalManualQA` against the `qa-rich` dataset, the non-prod Cognito email OTP flow, and the local QA database
- A passing fixture-preview harness alone does not close Slice 1 acceptance.

## Source of Truth

- `hidden-adventures-plan` defines scope, flow boundaries, and acceptance criteria.
- `v0-hidden-adventures-ui` is the canonical visual reference for Slice 1 parity work.
- `hidden-adventures-ios` owns native implementation details, test instrumentation, and explicit native behavior overrides.

## Integration Priority

- keep the live server runtime stable for email OTP auth entry, auth bootstrap, handle selection, viewer profile read/write, feed, detail, and profile
- keep explicit scheme-based environment switching stable for manual QA, automation, and production
- keep the onboarding-versus-linked routing split explicit: new users continue to onboarding/profile setup, linked users skip to Feed
- keep persisted-session relaunch and logout behavior stable in the supported Slice 1 auth flow
- preserve direct-launch and walkthrough UI test coverage in fixture-preview mode
- validate the live local happy path explicitly against the sibling server
- remove temporary live fallbacks only when the corresponding server contracts are locked

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
  - validate the local automation happy path against the real server
  - validate the manual QA path against the local Cognito-backed server mode when email OTP auth wiring is ready
  - validate the new-user onboarding path
  - validate the linked-user direct-login path
  - validate persisted-session relaunch into Feed

## Done Means

- slice-specific acceptance criteria are met
- app builds locally in Xcode
- Slice 1 is no longer fixture-backed for its core happy path
- real auth/bootstrap wiring includes email OTP session persistence, logout handling, post-auth routing into onboarding or Feed, and schema-backed profile persistence for new users
- linked issue and PR are closed
