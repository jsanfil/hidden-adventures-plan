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

## Done Means

- local stack runs on laptop
- initial contracts are documented
- release slice 1 server endpoints are ready for client integration

## Current State

- The server repo now has published `public` application tables backed by a repeatable migration pipeline from the legacy Mongo archive.
- Read-only slice 1 endpoints are implemented and verified for:
  - `GET /api/feed`
  - `GET /api/adventures/:id`
  - `GET /api/profiles/:handle`
- Endpoint reads already use the rebuilt visibility model against the published relational tables.
- The remaining backend-platform gap is to lock the contract docs from the implemented response shapes and replace the temporary `viewerHandle` query param with Cognito-backed viewer resolution.
