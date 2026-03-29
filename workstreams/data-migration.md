# Workstream: Data Migration

## Goal

Move legacy Mongo-backed data and existing media references into the new relational system safely and repeatably, then close the workstream once the published dataset is reconciled.

## Scope

- legacy inventory
- field mapping
- id mapping
- image validation
- reconciliation notes

## Deliverables

- [x] collection-by-collection inventory
- [x] legacy-to-new mapping document
- [x] dry-run import design
- [x] reconciliation checklist
- [x] published local dataset

## Dependencies

- backend schema direction
- access to the canonical legacy archive

## Reference

- [migration/legacy-inventory.md](../migration/legacy-inventory.md)
- [migration/archive-profile.md](../migration/archive-profile.md)
- [migration/legacy-to-new-mapping.md](../migration/legacy-to-new-mapping.md)
- [migration/postgresql-import-flow.md](../migration/postgresql-import-flow.md)
- [migration/cognito-account-linking-findings.md](../migration/cognito-account-linking-findings.md)
- [migration/reconciliation-checklist.md](../migration/reconciliation-checklist.md)
- [workstreams/backend-schema-draft.md](./backend-schema-draft.md)

## Available Legacy Source

- Full legacy Mongo export archive is available locally as:
  `/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/hidden-adventures-plan/migration/archives/legacy-mongodb-backup-2026-03-01.archive`
- Archive format appears to be a `mongodump --archive` style export from Mongo tools `r3.6.5`
- Collections visible in the archive include `adventures`, `profiles`, `comments`, `favorites`, `sidekicks`, `messages`, and `filenames`

## Done Means

- dry-run migration can be executed repeatedly
- counts and spot checks reconcile
- known data-risk areas are documented
- the workstream can be treated as closed for active program planning

## Current State

- The server repo supports:
  - raw archive staging into `migration_stage`
  - normalized transformation into `migration_work`
  - publish into the real `public` application tables
  - reconciliation reporting against the published dataset
- Import run `2` from the canonical legacy archive is currently published and reconciled for row counts.
- Imported legacy users are linked in the local rebuild DB to the live Cognito pool by exact handle with a stable `2598 / 2598` mapping.
- A saved unmatched Cognito account list exists for the `1383` pool users that do not correspond to a published legacy profile:
  `migration/reports/cognito-unmatched-users-2026-03-28.json`
- A formal reconciliation artifact exists in:
  `migration/reconciliation-checklist.md`
- Current audited skips for run `2` are:
  - `3` duplicate profile rows
  - `1` adventure with an unresolved author
  - `186` sidekick rows skipped or collapsed during canonical connection import
  - `89` favorites skipped due to unresolved or duplicate rows
  - `5` comments skipped due to unresolved or invalid rows

## Follow-Up Boundary

- This workstream is complete for active implementation planning.
- Any future S3 inventory verification should be treated as cutover validation rather than migration-workstream scope.
- Migration facts remain a dependency for Slice 1 integration and cutover planning, but migration itself is not an active parallel execution thread.
