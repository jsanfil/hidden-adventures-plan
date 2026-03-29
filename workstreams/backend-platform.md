# Workstream: Backend Platform

## Goal

Build the new relational backend, hybrid API, and local-first cloud deployment foundation.

## Scope

- domain model
- PostgreSQL + PostGIS schema
- hybrid API contracts
- Docker-based local stack
- cloud deployment shape
- auth and media integration

## Deliverables

- [x] schema draft
- [ ] API surface draft
- [x] local Docker stack
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
- initial contracts are documented
- release slice 1 server endpoints are ready for client integration

## Current State

- The server repo now has published `public` application tables backed by a repeatable migration pipeline from the legacy Mongo archive.
- The local rebuild DB now has a fully linked legacy identity set: `2598` imported users/profiles bound to Cognito by exact handle and `1383` extra Cognito accounts intentionally left unmatched.
- Read-only slice 1 endpoints are implemented and verified for:
  - `GET /api/feed`
  - `GET /api/adventures/:id`
  - `GET /api/profiles/:handle`
- Endpoint reads already use the rebuilt visibility model against the published relational tables.
- Read visibility now resolves the viewer from Cognito-backed auth context and uses local `users.id`, while public profile lookup remains handle-based.
- Bulk reconciliation is now handle-only by design. Verified-email matching remains a runtime legacy-account claim capability, not a migration primitive.
- The remaining backend-platform gap is to lock the contract docs from the implemented response shapes and continue expanding authenticated endpoint coverage without reintroducing handle-based viewer identity.
