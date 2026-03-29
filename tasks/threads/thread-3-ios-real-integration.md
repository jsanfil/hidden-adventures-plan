# Thread 3: Slice 1 iOS Real Integration

## Owning Repo

- `hidden-adventures-ios`

## Recommended Branch

- `codex/slice1-ios-real-integration`

## Mission

Replace the fixture-backed Slice 1 services with real server-backed integration and auth/bootstrap wiring while preserving the existing UI shell and UI-test harness.

## Allowed Scope

- network service layer
- auth bootstrap and handle-selection wiring
- app-shell integration required for Slice 1 happy path
- UI-harness adjustments required to preserve deterministic coverage
- repo-local iOS docs as needed

## Blocked Scope

- redefining server contracts on your own
- broad Slice 2 UI work
- redesigning the Slice 1 shell when the real issue is data integration
- deleting the fixture-backed path without a safe fallback plan during the transition

## Inputs

- thread 2 contract handoff
- current SwiftUI shell
- current UI gallery and walkthrough harness

## Deliverables

- real network-backed Slice 1 flow
- auth/bootstrap integration
- preserved or updated UI harness notes

## Required Checks

- simulator build
- `Scripts/run_ui_gallery.sh`
- local happy path across auth bootstrap, feed, detail, and profile
- document any intentional temporary fallback left in place

## Startup Prompt

You are Thread 3 for the Hidden Adventures rebuild. Work only in `hidden-adventures-ios` on branch `codex/slice1-ios-real-integration`. Replace the fixture-backed Slice 1 services with real server-backed integration using the locked contracts from Thread 2. Do not invent server behavior. Preserve the current UI-gallery and walkthrough harness as part of the acceptance path. Keep any temporary fallback explicit and documented.

## Handoff Format

- what fixture-backed paths were replaced
- what still depends on fixtures, if anything
- build and UI-harness results
- any server-side blockers or contract mismatches discovered
