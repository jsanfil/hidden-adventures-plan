# Hidden Adventures Rebuild Program

## Summary

- Run the modernization as a brand-new rebuild program, not inside the legacy repos.
- Use this repo as the global control tower for roadmap, release slices, decisions, migration closure, and cross-repo execution status.
- Optimize the next milestone around Slice 1 hardening and integration rather than broad early-phase foundation work.

## Program Repos

- `hidden-adventures-plan`
- `hidden-adventures-ios`
- `hidden-adventures-server`
- `hidden-adventures-api-tests`
- `v0-hidden-adventures-ui`

## Current Program State

### Completed

- rebuild workspace and sibling repos created
- legacy audit and preservation completed
- relational schema direction and visibility model established
- local-first Docker development environment bootstrapped
- migration tooling implemented from stage to transform to publish
- canonical legacy archive imported and reconciled locally
- Cognito reconciliation completed for published legacy identities
- Slice 1 visual design exploration established in `v0-hidden-adventures-ui`
- Slice 1 native SwiftUI shell implemented with a deterministic UI gallery and walkthrough harness
- Slice 1 server read endpoints implemented and tested
- auth bootstrap and handle-selection endpoints implemented and tested

### In Progress

- Slice 1 contract lock from real server response shapes
- iOS real API integration and auth/bootstrap wiring
- release acceptance documentation for Slice 1
- deployment and staging baseline

### Not Started / Later

- Slice 2 create, edit, upload, and visibility execution
- Slice 3 social engagement expansion
- Slice 4 support, moderation, beta, and cutover

## Program Principles

- Keep the PRD as the baseline feature floor, not the UI blueprint.
- Keep Cognito and S3 in phase 1 for continuity and lower migration risk.
- Use a relational domain model with PostgreSQL + PostGIS.
- Use a hybrid API, not resource-pure CRUD for every workflow.
- Replace ACL arrays with explicit visibility and connection policies.
- Prefer local-first development and production parity via containers.
- Do not let thread-level experimentation silently change scope, contracts, or navigation without flowing back through this repo.

## Auth Strategy

- Keep the current Cognito user pool as the legacy credential source; do not replace the pool and force a password migration.
- Treat `users.cognito_subject` as the durable backend identity key and `users.handle` as the public app alias.
- Keep username/password as a legacy compatibility path only; new-account auth should not be username/password-first.
- New-account priority for the rebuild is email plus Apple/Google, with phone-primary auth deferred to a later slice.
- Face ID and biometrics are a device-side session unlock mechanism after account linking, not a separate Cognito identity mode.
- Legacy users who still know their old credentials can sign in through the existing pool and complete a first-login upgrade or bootstrap flow.
- Legacy users who do not remember username or password should reclaim their old app identity through a verified-email recovery flow at runtime, not through bulk migration heuristics.
- Bulk Cognito reconciliation is intentionally stricter than runtime recovery: migration links imported users by exact Cognito `username -> users.handle` and skips everything else.
- New users who do not reclaim a legacy profile should create a fresh rebuild account and choose a unique public `handle` during onboarding.
- Prefer extending the existing pool with a rebuild app client and Apple/Google federation rather than creating a brand-new pool.

## Active Codex Threads

| Thread | Status | Primary Repo(s) | Owns | Produces | Depends On |
| --- | --- | --- | --- | --- | --- |
| Program control and doc sync | Active | `hidden-adventures-plan` | roadmap truth, slice docs, milestone board, cross-repo status sync | current-state snapshot, thread handoff notes, acceptance criteria | verified repo facts only |
| Slice 1 contract lock | Active | `hidden-adventures-server`, `hidden-adventures-api-tests`, `hidden-adventures-plan` | server contract docs, manual Postman assets that track the live API, small contract-safe server refinements | locked payload docs, updated Postman requests for troubleshooting, gap list for iOS integration | implemented server endpoints |
| Slice 1 iOS real integration | Ready after contract lock | `hidden-adventures-ios` | network services, auth bootstrap wiring, server-backed Slice 1 flows | local server-backed device and simulator flows | locked Slice 1 contracts |
| Deployment and staging baseline | Active | `hidden-adventures-server` | image versioning, env and secrets docs, deploy and rollback checklists, staging smoke flow | staging validation path and ops checklist | local server runtime foundation |
| Slice 2 product and UX incubation | Active | `hidden-adventures-plan`, `v0-hidden-adventures-ui` | create and edit flows, visibility UX, screen-map expansion | implementation-ready Slice 2 spec and visual references | Slice 1 scope stability |

## Release Slices

- Slice 1: auth bootstrap, profile bootstrap, feed, map, detail, image delivery
- Slice 2: create and edit adventure, uploads, location and category, visibility controls
- Slice 3: connections, favorites, comments, ratings, profile collections
- Slice 4: support and reporting, delete-account, moderation and admin, beta, cutover

## Current Implementation Snapshot

- Server migration tooling can stage the legacy Mongo archive, transform it into normalized work tables, publish a selected import run into the real `public` tables, and emit reconciliation reports.
- Import run `2` is currently published from the canonical archive and populates `public.users`, `public.profiles`, `public.adventures`, `public.connections`, `public.adventure_favorites`, `public.adventure_comments`, `public.media_assets`, `public.adventure_media`, and `public.adventure_stats`.
- Imported legacy profiles are fully linked in the local rebuild DB to Cognito by exact handle, with `2598` linked legacy users and `1383` extra Cognito accounts intentionally left unmatched.
- The server now exposes the real Slice 1 server surface for:
  - `GET /api/auth/bootstrap`
  - `POST /api/auth/handle`
  - `GET /api/feed`
  - `GET /api/adventures/:id`
  - `GET /api/profiles/:handle`
- Those endpoints are backed by Vitest coverage and reject the retired `viewerHandle` query-param pattern.
- `handle` is the public username for profile lookup and display; it is stable in v1 and separate from both `displayName` and Cognito `username`.
- A dedicated `v0-hidden-adventures-ui` repo exists as the Slice 1 visual design exploration and reference source.
- `hidden-adventures-ios` contains a native SwiftUI Slice 1 UI flow for welcome, profile setup, unified explore feed and map, and adventure detail.
- The iOS repo includes an XCTest-driven simulator gallery and walkthrough harness with deterministic launch routes, screenshot capture, and parity checks for Slice 1 UI work.
- The remaining Slice 1 gap is end-to-end integration: the iOS app still runs against fixture-backed services rather than the real server and auth bootstrap flow.

## Next Milestone Focus

- lock the Slice 1 contract from the implemented server surface
- update API-test assets to authenticated viewer behavior
- replace iOS fixture-backed Slice 1 services with real network clients
- validate the local end-to-end happy path across auth bootstrap, feed, detail, and profile
- stand up the first staging and rollback baseline

## Tracking Rules

- Every major task should map to an issue.
- Every issue should declare scope, owner repo, dependencies, acceptance criteria, and linked branch or PR.
- Do not mark a task complete until the code or docs are merged and verified in the owning repo.
- Thread-level work that changes scope, contracts, or navigation must update this repo before or alongside the implementation merge.
