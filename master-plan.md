# Hidden Adventures Rebuild Program

## Summary

- Run the modernization as a brand-new rebuild program, not inside the legacy repos.
- Use this repo as the global control tower for roadmap, release slices, decisions, migration, and parallel work.
- Build and ship through separate sibling repos for iOS and server implementation.

## Program Repos

- `hidden-adventures-plan`
- `hidden-adventures-ios`
- `hidden-adventures-server`

## Phase Status

- [x] Step 1: Create the new rebuild workspace
- [ ] Step 2: Legacy audit and preservation
- [ ] Step 3: Product and UX architecture
- [ ] Step 4: Backend and data architecture
- [ ] Step 5: Local-first platform
- [ ] Step 6: Migration tooling
- [ ] Step 7: Vertical slice 1
- [ ] Step 8: Vertical slice 2
- [ ] Step 9: Vertical slice 3
- [ ] Step 10: Vertical slice 4 and cutover

## Program Principles

- Keep the PRD as the baseline feature floor, not the UI blueprint.
- Keep Cognito and S3 in phase 1 for continuity and lower migration risk.
- Use a relational domain model with PostgreSQL + PostGIS.
- Use a hybrid API, not resource-pure CRUD for every workflow.
- Replace ACL arrays with explicit visibility and connection policies.
- Prefer local-first development and production parity via containers.

## Auth Strategy

- Keep the current Cognito user pool as the legacy credential source; do not replace the pool and force a password migration.
- Treat `users.cognito_subject` as the durable backend identity key and `users.handle` as the public app alias.
- Keep username/password as a legacy compatibility path only; new-account auth should not be username/password-first.
- New-account priority for the rebuild is email plus Apple/Google, with phone-primary auth deferred to a later slice.
- Face ID and biometrics are a device-side session unlock mechanism after account linking, not a separate Cognito identity mode.
- Legacy users who still know their old credentials can sign in through the existing pool and complete a first-login upgrade/bootstrap flow.
- Legacy users who do not remember username or password should reclaim their old app identity through a verified-email recovery flow at runtime, not through bulk migration heuristics.
- Bulk Cognito reconciliation is intentionally stricter than runtime recovery: migration links imported users by exact Cognito `username -> users.handle` and skips everything else.
- New users who do not reclaim a legacy profile should create a fresh rebuild account and choose a unique public `handle` during onboarding.
- Prefer extending the existing pool with a rebuild app client and Apple/Google federation rather than creating a brand-new pool.

## Parallel Workstreams

| Workstream | Status | Primary Repo | Can Run In Parallel With | Blockers |
| --- | --- | --- | --- | --- |
| Product/UX | Active | hidden-adventures-plan | iOS foundation, deployment setup | none |
| iOS foundation | Seeded | hidden-adventures-ios | Product/UX, deployment setup | none |
| Backend/domain/API | Active | hidden-adventures-server | Product/UX, deployment setup | Cognito-backed viewer resolution |
| Data migration | Active | hidden-adventures-plan | deployment setup | rollback checklist, media verification |
| Deploy/dev environment | Bootstrapped | hidden-adventures-server | Product/UX, backend/domain/API | none |

## Release Slices

- Slice 1: auth bootstrap, profile bootstrap, feed, map, detail, image delivery
- Slice 2: create/edit adventure, uploads, location/category, visibility controls
- Slice 3: connections, favorites, comments, ratings, profile collections
- Slice 4: support/reporting, delete-account, moderation/admin, beta, cutover

## Tracking Rules

- Every major task should map to an issue.
- Every issue should declare scope, owner repo, dependencies, acceptance criteria, and linked branch or PR.
- Do not mark a task complete until the code change is merged and verified.

## Next Actions

- [x] Complete the legacy inventory in [migration/legacy-inventory.md](./migration/legacy-inventory.md)
- [x] Start the product and UX workstream in [workstreams/product-ux.md](./workstreams/product-ux.md)
- [x] Draft the relational backend schema in [workstreams/backend-schema-draft.md](./workstreams/backend-schema-draft.md)
- [ ] Lock the slice 1 API surface in [workstreams/backend-platform.md](./workstreams/backend-platform.md) from the now-running feed/detail/profile endpoints
- [ ] Produce the navigation and screen map in [workstreams/product-ux.md](./workstreams/product-ux.md)
- [x] Draft the legacy-to-new data mapping document in [migration/legacy-to-new-mapping.md](./migration/legacy-to-new-mapping.md)
- [x] Draft the PostgreSQL import flow and staging strategy in [migration/postgresql-import-flow.md](./migration/postgresql-import-flow.md)
- [x] Resolve the account-linking strategy for imported users
- [x] Validate the imported-user account-linking strategy against the legacy iOS client and the live Cognito pool
- [ ] Finish the end-to-end migration playbook with rollback and reconciliation checklists
- [x] Acquire the full legacy Mongo archive for migration planning
- [x] Bootstrap the Xcode project in the iOS repo
- [x] Install server dependencies
- [x] Install Docker locally and bring up the server local stack

## Current Implementation Snapshot

- Server migration tooling can now stage the legacy Mongo archive, transform it into normalized work tables, publish a selected import run into the real `public` tables, and emit reconciliation reports.
- Import run `2` is currently published from the canonical archive and populates `public.users`, `public.profiles`, `public.adventures`, `public.connections`, `public.adventure_favorites`, `public.adventure_comments`, `public.media_assets`, `public.adventure_media`, and `public.adventure_stats`.
- Imported legacy profiles are now fully linked in the local rebuild DB to Cognito by exact handle, with `2598` linked legacy users and `1383` extra Cognito accounts intentionally left unmatched.
- The server now exposes the first read-only slice endpoints: `GET /api/feed`, `GET /api/adventures/:id`, and `GET /api/profiles/:handle`.
- Those endpoints now resolve authenticated viewers from Cognito-backed auth context and enforce visibility using local `users.id`.
- `handle` is the public username for profile lookup and display; it is stable in v1 and separate from both `displayName` and Cognito `username`.
- Bulk Cognito reconciliation is now intentionally handle-only; email is reserved for runtime legacy-account claim and recovery flows.
- The detailed identity and migration findings now live in [migration/cognito-account-linking-findings.md](./migration/cognito-account-linking-findings.md).
