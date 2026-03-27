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
