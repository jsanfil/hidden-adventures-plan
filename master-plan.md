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

## Execution Model

- Run Codex work in parallel across repos, not as multiple active implementation threads in the same repo.
- Use each repo's `main` branch directly unless there is a repo-specific reason not to.
- Keep `hidden-adventures-plan` as the control tower for milestone status, release notes, and cross-repo truth.
- Require every repo lane to end each cycle with a short handoff covering what changed, what is now stable, what another repo may rely on, and what remains unresolved.
- Treat Vitest as the official server verification path and Postman as a manual troubleshooting companion only.

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
- Slice 1 contract docs and Postman troubleshooting requests now reflect the implemented server surface and auth model
- the testing and environment operating model now distinguishes local manual QA from local automation, with separate local databases and manifest-driven fixture packs
- Slice 1 iOS runtime now defaults to server-backed auth/bootstrap, feed, detail, and profile clients while fixture preview remains explicit for the UI harness
- first deployment baseline is checked in with image versioning guidance, env templates, rollout and rollback notes, and a staging smoke script
- the worktree-based thread setup has been retired in favor of repo-based execution on `main`

### In Progress

- local live-runtime Slice 1 acceptance across auth bootstrap, feed, detail, and profile
- release acceptance documentation for Slice 1
- first staging smoke execution from the deployment baseline

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
- Do not let repo-level implementation drift silently change scope, contracts, or navigation without flowing back through this repo.

## Auth Strategy

- Keep the current production Cognito user pool for live users; do not replace the pool now that the existing pool supports the rebuild auth direction.
- Use a separate non-production Cognito pool and app client for local manual QA.
- Treat `users.cognito_subject` as the durable backend identity key and `users.handle` as the public app alias.
- Use email plus one-time code as the app's visible auth method for both new and existing users.
- Reuse the current production pool with verified email alias sign-in, `EMAIL_OTP` first-factor support, and a rebuild-capable app client with `ALLOW_USER_AUTH`.
- Manual-QA Cognito sign-up currently has an observed non-prod pool constraint: after an email address has already been used for sign-up confirmation testing, deleting and recreating that Cognito user may still fail to trigger a new confirmation email to the same address. Until AWS behavior proves otherwise, manual QA for `Get Started` should use a brand-new email address when confirmation delivery fails on a reused address.
- Gmail can separately filter or suppress confirmation mail from the Cognito sender `no-reply@verificationemail.com`, so a missing code in Gmail should be treated as an email-delivery issue before assuming Cognito failed to send.
- `Get Started` is the onboarding-intent path, but onboarding should only continue after verified auth when bootstrap returns `new_user_needs_handle`.
- `Sign In` is the returning-user path, but the backend remains authoritative after verified auth and may still identify the user as new.
- New users should create a fresh rebuild account and choose a unique public `handle` during onboarding.
- Existing linked users, including migrated legacy users, should resolve by `users.cognito_subject` and skip onboarding/profile setup.
- Username/password and runtime recovery are out of scope for the rebuild app unless live production validation reveals a blocker severe enough to justify a temporary fallback.
- Face ID and biometrics are a device-side session unlock mechanism after account linking, not a separate Cognito identity mode.
- Bulk Cognito reconciliation remains a historical migration concern: imported legacy users are already linked in the rebuild dataset and runtime auth now depends on those existing `cognito_subject` mappings.
- Apple and Google federation remain future pool/app-client extensions rather than a Slice 1 requirement.
- Use deterministic signed test JWTs for automated local regression instead of depending on live Cognito tokens.

## Active Repo Lanes

| Lane | Status | Primary Repo | Owns | Produces | Depends On |
| --- | --- | --- | --- | --- | --- |
| Planning and doc sync | Active | `hidden-adventures-plan` | roadmap truth, slice docs, milestone board, cross-repo status sync | current-state snapshot, lane handoff notes, acceptance criteria | verified repo facts only |
| Backend and ops | Active | `hidden-adventures-server` | locked Slice 1 server surface, local acceptance support, staging smoke execution | passing server checks, deploy and smoke notes, contract-safe server follow-up | implemented server endpoints and deploy assets |
| App integration and acceptance | Active | `hidden-adventures-ios` | live-runtime validation, fallback inventory, UI-harness stability | local server-backed runtime notes, passing UI harness, live acceptance findings | locked Slice 1 contracts |
| Manual API troubleshooting assets | On demand | `hidden-adventures-api-tests` | Postman requests that mirror the live API for troubleshooting | updated troubleshooting collections and environment notes | server contract changes only |
| Slice 2 product and UX definition | Active | `v0-hidden-adventures-ui` | create and edit flows, visibility UX, screen-map expansion | implementation-ready Slice 2 visual references and screen maps | Slice 1 scope stability |

## Release Slices

- Slice 1: email OTP auth entry, auth bootstrap, handle selection, new-user onboarding/profile bootstrap, feed, map, detail, image delivery
- Slice 2: create and edit adventure, uploads, location and category, visibility controls
- Slice 3: connections, favorites, comments, ratings, profile collections
- Slice 4: support and reporting, delete-account, moderation and admin, beta, cutover

## Current Implementation Snapshot

- Server migration tooling can stage the legacy Mongo archive, transform it into normalized work tables, publish a selected import run into the real `public` tables, and emit reconciliation reports.
- Import run `2` is currently published from the canonical archive and populates `public.users`, `public.profiles`, `public.adventures`, `public.connections`, `public.adventure_favorites`, `public.adventure_comments`, `public.media_assets`, `public.adventure_media`, and `public.adventure_stats`.
- Imported legacy profiles are fully linked in the local rebuild DB to Cognito by exact handle, and the published rebuild dataset now treats `users.cognito_subject` as the durable identity bridge for those existing users.
- The server now exposes the real Slice 1 server surface for:
  - `GET /api/auth/bootstrap`
  - `POST /api/auth/handle`
  - `GET /api/me/profile`
  - `PUT /api/me/profile`
  - `GET /api/feed`
  - `GET /api/adventures/:id`
  - `GET /api/profiles/:handle`
- Those endpoints are backed by Vitest coverage, reject the retired `viewerHandle` query-param pattern, and now require bearer auth for every business route except `GET /api/health`.
- The current production Cognito pool has been verified for the rebuild auth path: email is an alias sign-in attribute, `EMAIL_OTP` is enabled as a first auth factor, and the rebuild app client supports `ALLOW_USER_AUTH`.
- Local manual-QA auth now includes an additional operator note for Cognito sign-up testing: a reused email address can stop receiving a new confirmation email even after its deleted Cognito user is recreated, so fresh addresses are the reliable path for `Get Started` validation.
- Gmail-specific filtering of `no-reply@verificationemail.com` means confirmation delivery should be verified in another inbox or provider before treating it as a Cognito sender failure.
- Local testing now splits into two explicit runtime modes:
  - `local-manual-qa` uses the `hidden_adventures_qa` database, the `qa-rich` manifest pack, real non-prod Cognito email OTP auth, and real non-prod S3
  - `local-automation-test-core` uses the `hidden_adventures_test` database, the `test-core` manifest pack, and deterministic signed test JWTs
- The canonical cross-repo operating model for testing, fixtures, local databases, AWS separation, and manual tester workflow lives in [workstreams/testing-environments.md](./workstreams/testing-environments.md).
- The Postman Native Git repo includes checked-in Slice 1 troubleshooting requests under `postman/collections/hidden-adventures-slice-1/` that use bearer auth for connected-viewer paths instead of `viewerHandle`.
- `handle` is the public username for profile lookup and display; it is stable in v1 and separate from both `displayName` and Cognito `username`.
- A dedicated `v0-hidden-adventures-ui` repo exists as the Slice 1 visual design exploration and reference source.
- `hidden-adventures-ios` contains a native SwiftUI Slice 1 UI flow for welcome, unified email-auth entry, code verification, new-user onboarding/profile setup, unified explore feed and map, and adventure detail.
- The iOS repo now supports explicit `LocalManualQA`, `LocalAutomation`, and `Production` server modes, while the XCTest-driven gallery and walkthrough harness remain in explicit fixture-preview mode for deterministic screenshots and acceptance captures.
- Slice 1 auth now includes additional runtime behavior beyond bootstrap alone: persisted sessions relaunch directly into Explore/Feed, logout clears the local session and requires email OTP on next entry, and onboarding intent only applies to users who bootstrap as `new_user_needs_handle`.
- Profile setup now persists meaningful user information beyond handle selection through `GET /api/me/profile` and `PUT /api/me/profile`, covering `displayName`, `bio`, `homeCity`, and `homeRegion`.
- Deployment artifacts now live in `hidden-adventures-server/deploy/`, including env templates, a staging compose example, and a smoke script for root, health, feed, detail, profile, and optional auth checks.
- The remaining Slice 1 gap is acceptance closure rather than basic implementation: the live runtime still needs explicit happy-path validation for new-user onboarding, linked-user direct sign-in, persisted session relaunch, and the documented staging smoke path still needs its first real execution.

## Next Milestone Focus

- keep the repo-based operating model simple: one active implementation thread per repo on `main`
- validate the local manual-QA happy path across email OTP auth entry, auth bootstrap, onboarding, feed, detail, and profile using the dedicated non-prod Cognito flow
- validate the local automation happy path against the deterministic `test-core` dataset and test JWT auth
- execute the first staging smoke run from the checked-in deployment baseline
- close the remaining Slice 1 acceptance notes around manual QA for new-user onboarding, linked-user sign-in, persisted-session relaunch, authenticated media delivery, and map behavior
- keep Slice 2 in UX and spec definition only until Slice 1 acceptance is closed

## Tracking Rules

- Every major task should map to an issue.
- Every issue should declare scope, owner repo, dependencies, acceptance criteria, and the linked commit, PR, or merged artifact that proves status.
- Do not mark a task complete until the code or docs are merged and verified in the owning repo.
- Repo-lane work that changes scope, contracts, or navigation must update this repo before or alongside the implementation merge.
