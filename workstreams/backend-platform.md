# Workstream: Backend Platform

## Goal

Build the new relational backend, hybrid API, and local-first cloud deployment foundation, with the immediate focus on locking the implemented Slice 1 contracts and supporting real client integration.

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
- [ ] contract documentation from implemented response shapes
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
- Read endpoints already use the rebuilt visibility model against the published relational tables.
- Authenticated viewer resolution now comes from Cognito-backed auth context and local `users.id`.
- `viewerHandle` is retired as a client-facing planning primitive and should only appear in negative tests that enforce its removal from the public interface.
- Bulk reconciliation is handle-only by design. Verified-email matching remains a runtime legacy-account claim capability, not a migration primitive.

## Next Output

- lock the contract docs from the implemented payloads and auth expectations
- keep authenticated endpoint growth additive and integration-friendly
- support the iOS thread without reintroducing handle-based viewer identity
