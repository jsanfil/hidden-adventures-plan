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

## Parallel Workstreams

| Workstream | Status | Primary Repo | Can Run In Parallel With | Blockers |
| --- | --- | --- | --- | --- |
| Product/UX | Active | hidden-adventures-plan | iOS foundation, deployment setup | none |
| iOS foundation | Seeded | hidden-adventures-ios | Product/UX, deployment setup | none |
| Backend/domain/API | Active | hidden-adventures-server | Product/UX, deployment setup | API surface draft |
| Data migration | Ready To Start | hidden-adventures-plan | deployment setup | representative legacy extracts |
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
- [ ] Draft the slice 1 API surface in [workstreams/backend-platform.md](./workstreams/backend-platform.md)
- [ ] Produce the navigation and screen map in [workstreams/product-ux.md](./workstreams/product-ux.md)
- [ ] Start the legacy-to-new data mapping document in [workstreams/data-migration.md](./workstreams/data-migration.md)
- [x] Bootstrap the Xcode project in the iOS repo
- [x] Install server dependencies
- [x] Install Docker locally and bring up the server local stack
