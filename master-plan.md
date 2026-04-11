# Hidden Adventures Rebuild Program

## Summary

- Run the modernization as a brand-new rebuild program, not inside the legacy repos.
- Use this repo as the global control tower for roadmap, feature sequencing, decisions, migration closure, and cross-repo execution status.
- Keep Slice 1 as the only bundled milestone that is already complete.
- Deliver the rest of the product one major feature at a time instead of planning another large implementation slice.
- Treat `archive/` as historical context only. It is not authoritative for current status, sequencing, or repo-next decisions.

## Program Repos

- `hidden-adventures-plan`
- `hidden-adventures-ios`
- `hidden-adventures-server`
- `hidden-adventures-api-tests`
- `v0-hidden-adventures-ui`

## Execution Model

- Run Codex work in parallel across repos, and allow multiple active threads or worktrees inside a repo when scopes are explicit and non-conflicting.
- Use each repo's `main` branch directly unless there is a repo-specific reason not to.
- Keep `hidden-adventures-plan` as the control tower for feature status, release notes, and cross-repo truth.
- Require every repo lane to end each cycle with a short handoff covering what changed, what is now stable, what another repo may rely on, and what remains unresolved.
- Treat Vitest as the official server verification path and Postman as a manual troubleshooting companion only.
- Use [workstreams/v0-screen-porting-workflow.md](./workstreams/v0-screen-porting-workflow.md) as the repeatable pattern for any remaining screen port from `v0-hidden-adventures-ui` into `hidden-adventures-ios`.

## Planning Model

The active operating model separates three different planning questions:

- `Program Priority Order`
  The canonical feature sequence for product delivery.
- `Repo-Autonomous Next Work`
  The allowed next work for each repo, including preparatory work that may happen ahead of the top-priority feature when it is additive, assumption-driven, and does not silently redefine accepted shipped scope.
- `Active Threads`
  The currently open execution units, including optional parallel threads or separate git worktrees inside the same repo. These are coordination artifacts, not the source of truth for sequencing.

Use `master-plan.md`, `features/`, `workstreams/`, and `tasks/parallel-tracks.md` for current planning decisions. Do not use `archive/` to decide what is next.

## Feature Delivery Loop

Every remaining major feature should move through the same implementation loop:

1. Design the feature or view in `v0-hidden-adventures-ui`.
2. Build the SwiftUI version in `hidden-adventures-ios` with mock or fixture data and iterate until the UI is accepted.
3. Implement any required server APIs in `hidden-adventures-server`.
4. Wire the iOS app to the live APIs and keep the fixture-backed path intact for UI coverage.

This loop is the recommended ship path for post-Slice-1 work unless a feature is purely operational. It does not forbid additive repo-local preparatory work ahead of the currently shipping feature.

## Feature Completion Standard

Each feature is complete only when all of these gates are satisfied:

- `Design accepted`
  v0 screens, screenshots, and UX notes are explicit enough for implementation.
- `Mock iOS accepted`
  SwiftUI fixture-backed implementation is visually accepted, gallery coverage is updated, and parity review against v0 is complete.
- `Server accepted`
  Required API additions are implemented and covered by server tests without silently changing completed feature contracts.
- `Integrated iOS accepted`
  The app is wired to the live APIs, fixture mode remains intact for UI coverage, and the local happy path works.
- `QA accepted`
  Automation and manual QA are recorded for the affected user journey at each step where they apply.

## Tracking Model

- `master-plan.md` is the program rollup and the only place that should summarize status across all major features.
- Each major feature has its own doc under `features/`.
- The feature doc is the source of truth for detailed scope, dependencies, gate checklists, and proof of completion.
- `tasks/parallel-tracks.md` is the source of truth for repo backlog rules and any optional registry of active threads or worktrees.
- A feature should be marked `Done` in this master plan only after its feature doc shows all completion gates satisfied and the linked repo work is merged and verified.
- Family-level docs are no longer the active unit of completion tracking.
- `archive/` is historical only and must not be used for current status, sequencing, or repo-next decisions.

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
- Slice 1 is complete under the current milestone definition: signup, login, basic feed, profile, and adventure detail now count as the release goal
- first deployment baseline is checked in with image versioning guidance, env templates, rollout and rollback notes, and a staging smoke script
- the worktree-based thread setup has been retired in favor of repo-based execution on `main`
- Create Adventure implementation, gallery coverage, server create path, and manual QA are complete

### In Progress

- first staging smoke execution from the deployment baseline
- post-Slice-1 planning restructure from slice-based execution to feature-by-feature delivery

### Later

- all remaining user-facing feature work listed in the execution order below
- LightSail staging hardening beyond the first smoke pass
- production-readiness validation and cutover preparation after the core feature set is complete

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
- Use email plus one-time code as the current app-visible auth method for both new and existing users until expanded auth is intentionally scheduled.
- Reuse the current production pool with verified email alias sign-in, `EMAIL_OTP` first-factor support, and a rebuild-capable app client with `ALLOW_USER_AUTH`.
- Manual-QA Cognito sign-up currently has an observed non-prod pool constraint: after an email address has already been used for sign-up confirmation testing, deleting and recreating that Cognito user may still fail to trigger a new confirmation email to the same address. Until AWS behavior proves otherwise, manual QA for `Get Started` should use a brand-new email address when confirmation delivery fails on a reused address.
- Gmail can separately filter or suppress confirmation mail from the Cognito sender `no-reply@verificationemail.com`, so a missing code in Gmail should be treated as an email-delivery issue before assuming Cognito failed to send.
- `Get Started` is the onboarding-intent path, but onboarding should only continue after verified auth when bootstrap returns `new_user_needs_handle`.
- `Sign In` is the returning-user path, but the backend remains authoritative after verified auth and may still identify the user as new.
- New users should create a fresh rebuild account and choose a unique public `handle` during onboarding.
- Existing linked users, including migrated legacy users, should resolve by `users.cognito_subject` and skip onboarding/profile setup.
- Username/password and runtime recovery are out of scope for the current auth baseline unless live production validation reveals a blocker severe enough to justify a temporary fallback.
- Face ID and biometrics are a device-side session unlock mechanism after account linking in the current baseline, not a separate identity mode.
- Apple, Google, phone-number auth, passkeys, and richer biometric sign-in are tracked as a dedicated later feature rather than incidental extensions of Slice 1.
- Bulk Cognito reconciliation remains a historical migration concern: imported legacy users are already linked in the rebuild dataset and runtime auth now depends on those existing `cognito_subject` mappings.
- Use deterministic signed test JWTs for automated local regression instead of depending on live Cognito tokens.

## Feature Rollup

| Order | Feature | Status | Feature Doc | Summary |
| --- | --- | --- | --- | --- |
| 1 | Create Adventure | Done | [features/create-adventure.md](./features/create-adventure.md) | authoring entry, metadata, primary media, location, category, visibility |
| 2 | Map Discovery + Location Search | In Progress | [features/map-discovery-location-search.md](./features/map-discovery-location-search.md) | real map plus vague-location search and 25-mile discovery scope |
| 3 | Connections + Profile Discovery | Not Started | [features/connections-profile-discovery.md](./features/connections-profile-discovery.md) | searchable profiles, connection states, connection-aware visibility value |
| 4 | Profile Collections | Not Started | [features/profile-collections.md](./features/profile-collections.md) | authored adventures and favorites on profile surfaces |
| 5 | Favorites | Not Started | [features/favorites.md](./features/favorites.md) | save and unsave flows plus saved-state rendering |
| 6 | Comments | Not Started | [features/comments.md](./features/comments.md) | comment list and composer on adventure detail |
| 7 | Ratings | Not Started | [features/ratings.md](./features/ratings.md) | rating interaction and rating display aggregates |
| 8 | Adventure Sharing + Friend Invites | Not Started | [features/adventure-sharing-friend-invites.md](./features/adventure-sharing-friend-invites.md) | shareable links, text/social share, contact-based invites |
| 9 | Expanded Authentication | Not Started | [features/expanded-authentication.md](./features/expanded-authentication.md) | phone, Google, Apple, passkeys, biometrics |
| 10 | Support, Reporting, And Account Management | Not Started | [features/support-reporting-account-management.md](./features/support-reporting-account-management.md) | support, reports, legal/settings, logout, delete-account |
| 11 | Edit Adventure | Not Started | [features/edit-adventure.md](./features/edit-adventure.md) | edit existing adventure content using the authoring foundation |

## Program Priority Order

- Product delivery should continue in the feature order listed above.
- `Create Adventure` remains the first ship-priority feature after completed Slice 1 work.
- Repos may perform preparatory work ahead of that ship order when the work is additive, assumptions are documented, and accepted feature behavior is not redefined.

## Repo-Autonomous Next Work

- `hidden-adventures-plan`
  Keep the feature order, repo backlog rules, thread registry, and archive guardrails current.
- `v0-hidden-adventures-ui`
  Prioritize design work for the top ship-priority feature first, but later-feature exploration is allowed when clearly marked provisional.
- `hidden-adventures-ios`
  Prioritize accepted-design fixture-backed implementation for the current ship feature, but reusable infrastructure and non-binding groundwork for later features may move ahead when they do not force product decisions.
- `hidden-adventures-server`
  May work ahead across multiple future features with evolving contracts, schema, endpoints, and tests, provided assumptions are documented, live contract docs stay accurate, regression coverage moves with the change, and affected iOS work is handed off explicitly.
- `hidden-adventures-api-tests`
  Follow only live server behavior. Do not publish speculative troubleshooting assets for future APIs that are not live yet.

## Active Threads

- Active execution can run as multiple parallel threads or git worktrees, including multiple threads inside the same repo.
- Active threads must stay inside documented scope and should map back to the program priority order, feature docs, and repo backlog rules.
- Use [tasks/parallel-tracks.md](./tasks/parallel-tracks.md) for the current thread registry pattern and [tasks/thread-template.md](./tasks/thread-template.md) when creating or recording a thread.

## Public Interface Expectations

Upcoming features are expected to add or expand public interfaces in these areas:

- `Discovery search`
  Feed and map will need a location search input, candidate-location selection, and a 25-mile location filter mode in addition to current-location default behavior.
- `Connections`
  Server support will be needed for profile search, connection state transitions, and connection-aware profile and adventure reads.
- `Sharing and invites`
  App and server support will be needed for shareable adventure links and invite flows; contacts access and text-share behavior should be planned as client capabilities with minimal server dependency unless referral tracking is added later.
- `Expanded auth`
  Auth work is a dedicated later feature, not an incidental extension of Slice 1. Federated identity, phone auth, passkeys, and biometrics should be treated as deliberate contract and QA expansions.

## Active Repo Lanes

| Lane | Status | Primary Repo | Owns | Produces | Depends On |
| --- | --- | --- | --- | --- | --- |
| Planning and doc sync | Active | `hidden-adventures-plan` | roadmap truth, feature inventory, milestone board, cross-repo status sync | current-state snapshot, feature sequencing notes, acceptance criteria | verified repo facts only |
| Backend and ops | Active | `hidden-adventures-server` | maintain the accepted current server contract, evolve live APIs for shipped features, and continue staging baseline follow-up | passing server checks, evergreen contract notes, deploy and smoke notes | implemented server endpoints and deploy assets |
| App integration and acceptance | Active | `hidden-adventures-ios` | preserve Slice 1 runtime stability, absorb accepted server contract updates, and execute the current scheduled feature loop without breaking fixture preview | local runtime notes, passing UI harness, integration findings | accepted current server contract plus approved feature contracts |
| Manual API troubleshooting assets | On demand | `hidden-adventures-api-tests` | Postman requests that mirror the live API for troubleshooting | updated troubleshooting collections and environment notes | server contract changes only |
| Feature UX definition | Active | `v0-hidden-adventures-ui` | design and refine the next scheduled feature before native implementation starts | approved visual references, screenshots, and screen-map notes | current feature selection and Slice 1 scope stability |

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
- `hidden-adventures-ios` contains a native SwiftUI Slice 1 UI flow for welcome, unified email-auth entry, code verification, new-user onboarding/profile setup, basic feed, profile, and adventure detail.
- The iOS repo now supports explicit `LocalManualQA`, `LocalAutomation`, and `Production` server modes, while the XCTest-driven gallery and walkthrough harness remain in explicit fixture-preview mode for deterministic screenshots and acceptance captures.
- Slice 1 auth now includes additional runtime behavior beyond bootstrap alone: persisted sessions relaunch directly into Explore/Feed, logout clears the local session and requires email OTP on next entry, and onboarding intent only applies to users who bootstrap as `new_user_needs_handle`.
- Profile setup now persists meaningful user information beyond handle selection through `GET /api/me/profile` and `PUT /api/me/profile`, covering `displayName`, `bio`, `homeCity`, and `homeRegion`.
- Deployment artifacts now live in `hidden-adventures-server/deploy/`, including env templates, a staging compose example, and a smoke script for root, health, feed, detail, profile, and optional auth checks.
- Slice 1 is closed under the current milestone definition, while the remaining feature inventory and the first staging smoke execution are tracked as later work.

## Later Operational Phase

After the core feature inventory is complete:

- run LightSail staging hardening and the full staging smoke cycle
- prepare production environment, secrets, and rollout safety checks
- execute final production-readiness validation
- plan cutover and post-launch follow-up

Operational readiness stays outside the per-feature implementation loop unless a specific feature depends on infrastructure that does not yet exist.

## Tracking Rules

- Every major task should map to an issue.
- Every issue should declare scope, owner repo, dependencies, acceptance criteria, and the linked commit, PR, or merged artifact that proves status.
- Do not mark a task complete until the code or docs are merged and verified in the owning repo.
- Repo-lane work that changes scope, contracts, or navigation must update this repo before or alongside the implementation merge.
