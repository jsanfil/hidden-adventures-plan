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
- [x] legacy-to-new mapping document
- [x] dry-run import design
- [ ] reconciliation checklist
- [ ] rollback checklist

## Dependencies

- backend schema direction
- access to the canonical legacy archive

## Reference

- [migration/legacy-inventory.md](../migration/legacy-inventory.md)
- [migration/archive-profile.md](../migration/archive-profile.md)
- [migration/legacy-to-new-mapping.md](../migration/legacy-to-new-mapping.md)
- [migration/postgresql-import-flow.md](../migration/postgresql-import-flow.md)
- [migration/cognito-account-linking-findings.md](../migration/cognito-account-linking-findings.md)
- [workstreams/backend-schema-draft.md](./backend-schema-draft.md)

## Available Legacy Source

- Full legacy Mongo export archive is available locally as:
  `/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/hidden-adventures-plan/migration/archives/legacy-mongodb-backup-2026-03-01.archive`
- Archive format appears to be a `mongodump --archive` style export from Mongo tools `r3.6.5`
- Collections visible in the archive include `adventures`, `profiles`, `comments`, `favorites`, `sidekicks`, `messages`, and `filenames`

## Immediate Next Steps

- turn the existing publish report into the formal reconciliation checklist artifact
- add spot-check reconciliation for visibility conversion, category normalization, and media key preservation
- document the rollback path for replacing published `public` data from a selected import run
- verify the media storage keys against the actual S3 inventory before cutover

## Done Means

- dry-run migration can be executed repeatedly
- counts and spot checks reconcile
- known data-risk areas are documented

## Current State

- The server repo now supports:
  - raw archive staging into `migration_stage`
  - normalized transformation into `migration_work`
  - publish into the real `public` application tables
  - reconciliation reporting against the published dataset
- Import run `2` from the canonical legacy archive is currently published and reconciled for row counts.
- Imported legacy users are now linked in the local rebuild DB to the live Cognito pool by exact handle with a stable `2598 / 2598` mapping.
- A saved unmatched Cognito account list now exists for the `1383` pool users that do not correspond to a published legacy profile:
  `migration/reports/cognito-unmatched-users-2026-03-28.json`
- Current audited skips for run `2` are:
  - `3` duplicate profile rows
  - `1` adventure with an unresolved author
  - `186` sidekick rows skipped or collapsed during canonical connection import
  - `89` favorites skipped due to unresolved or duplicate rows
  - `5` comments skipped due to unresolved or invalid rows
- The main remaining migration-planning work is to formalize the reconciliation checklist and rollback procedure, not to discover the source data or the legacy account-linking rule.
