# Workstream: Data Migration

## Goal

Move legacy Mongo-backed data and existing media references into the new relational system safely and repeatably.

## Scope

- legacy inventory
- field mapping
- id mapping
- image validation
- reconciliation and rollback notes

## Deliverables

- [x] collection-by-collection inventory
- [ ] legacy-to-new mapping document
- [ ] dry-run import design
- [ ] reconciliation checklist
- [ ] rollback checklist

## Dependencies

- backend schema direction
- access to representative legacy data

## Reference

- [migration/legacy-inventory.md](../migration/legacy-inventory.md)
- [workstreams/backend-schema-draft.md](./backend-schema-draft.md)

## Done Means

- dry-run migration can be executed repeatedly
- counts and spot checks reconcile
- known data-risk areas are documented
