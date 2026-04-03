# Workstream: Backend Platform

## Goal

Build the new relational backend, hybrid API, and local-first cloud deployment foundation, with the immediate focus on holding the locked Slice 1 contracts steady and supporting real client integration.

## Scope

- domain model
- PostgreSQL + PostGIS schema
- hybrid API contracts
- Docker-based local stack
- cloud deployment shape
- auth and media integration

## Deliverables

- [x] schema draft
- [x] implemented Slice 1 server surface
- [x] local Docker stack
- [x] contract documentation from implemented response shapes
- [ ] staging deployment path
- [ ] observability baseline

## Dependencies

- legacy audit
- product and UX decisions for social and visibility model

## Reference

- [workstreams/visibility-model.md](./visibility-model.md)
- [workstreams/backend-schema-draft.md](./backend-schema-draft.md)
- [migration/cognito-account-linking-findings.md](../migration/cognito-account-linking-findings.md)

## Done Means

- local stack runs on laptop
- initial contracts are documented from real endpoints
- release Slice 1 server endpoints are consumable by the iOS integration thread

## Current State

- The server repo has published `public` application tables backed by a repeatable migration pipeline from the legacy Mongo archive.
- The local rebuild DB has a fully linked legacy identity set: `2598` imported users and profiles bound to Cognito by exact handle and `1383` extra Cognito accounts intentionally left unmatched.
- The current Slice 1 server surface is implemented and tested for:
  - `GET /api/auth/bootstrap`
  - `POST /api/auth/handle`
  - `GET /api/feed`
  - `GET /api/adventures/:id`
  - `GET /api/profiles/:handle`
- The implemented Slice 1 surface is now mirrored by plan-repo contract notes and checked-in Postman Native Git troubleshooting requests under `hidden-adventures-api-tests/postman/collections/hidden-adventures-slice-1/`.
- The locked Slice 1 contract now requires bearer auth for every business route except `GET /api/health`.
- Local runtime now splits into:
  - `local-manual-qa`, which uses the `hidden_adventures_qa` database, a rich manifest-driven fixture pack, real non-prod Cognito, and real non-prod S3
  - `local-automation-test-core`, which uses the `hidden_adventures_test` database, a deterministic manifest-driven fixture pack, and signed test JWTs
- Read endpoints already use the rebuilt visibility model against the published relational tables.
- Authenticated viewer resolution now comes from auth context and local `users.id`, with Cognito for manual QA and production, and deterministic test JWTs for local automation.
- `viewerHandle` is retired as a client-facing planning primitive and should only appear in negative tests that enforce its removal from the public interface.
- Bulk reconciliation is handle-only by design. Verified-email matching remains a runtime legacy-account claim capability, not a migration primitive.
- The cross-repo environment and testing source of truth now lives in `workstreams/testing-environments.md`.

## Next Output

- keep the locked contract docs current if additive Slice 1-safe server changes land
- keep authenticated endpoint growth additive and integration-friendly
- support local manual-QA acceptance, local automation regression, and staging smoke work without reintroducing handle-based viewer identity
- record the first real staging smoke execution with the image identifier, runtime shape, smoke results, and any rollback friction
