# Migration Reconciliation Checklist

Historical note:

- This document records the completed migration bridge and unmatched-account audit as historical evidence.
- The unmatched Cognito-account artifacts remain useful migration records, but they are no longer treated as planned runtime-recovery inputs for the rebuild app flow.

## Goal

Record the concrete checks that justify closing the migration planning and implementation workstream for the rebuild dataset.

## Source and Publish Basis

- Canonical archive:
  `/Users/josephsanfilippo/Documents/projects/hidden-adventures-rebuild/hidden-adventures-plan/migration/archives/legacy-mongodb-backup-2026-03-01.archive`
- Archive inventory:
  [archive-profile.md](./archive-profile.md)
- Mapping rules:
  [legacy-to-new-mapping.md](./legacy-to-new-mapping.md)
- Import flow:
  [postgresql-import-flow.md](./postgresql-import-flow.md)
- Identity findings:
  [cognito-account-linking-findings.md](./cognito-account-linking-findings.md)

## Execution Checklist

- [x] Legacy archive acquired and profiled
- [x] Repeatable stage -> transform -> publish pipeline implemented
- [x] Import run `2` published into the rebuild `public` tables
- [x] Legacy-profile-backed users linked to Cognito by exact handle
- [x] Extra Cognito accounts preserved as unmatched instead of being auto-linked
- [x] Audited skips and collapses documented
- [x] Row counts reconcile against archive totals plus documented skips/collapses
- [x] Spot checks reconcile for visibility normalization and single-image media projection
- [x] Known migration risk areas documented

## Row-Count Reconciliation

### Archive counts

- `profiles`: `2630`
- `adventures`: `353`
- `sidekicks`: `1190`
- `favorites`: `1958`
- `comments`: `145`

### Final published counts

- `users`: `2598`
- `profiles`: `2598`
- `adventures`: `352`
- `connections`: `1004`
- `adventure_favorites`: `1869`
- `adventure_comments`: `140`
- `media_assets`: `1839`
- `adventure_media`: `352`
- `adventure_stats`: `352`

### Reconciled deltas

- Profiles:
  `2630` archive profiles
  minus `3` duplicate profile rows skipped during import
  minus `29` zero-activity duplicate legacy profiles intentionally removed from the rebuild dataset
  equals `2598` published users/profiles

- Adventures:
  `353` archive adventures
  minus `1` unresolved author
  equals `352` published adventures

- Sidekicks:
  `1190` archive rows
  minus `186` skipped or collapsed during canonical connection import
  equals `1004` published connections

- Favorites:
  `1958` archive rows
  minus `89` unresolved or duplicate rows
  equals `1869` published favorites

- Comments:
  `145` archive rows
  minus `5` unresolved or invalid rows
  equals `140` published comments

## Identity Reconciliation

- Published legacy users/profiles in rebuild DB: `2598`
- Linked Cognito subjects after final apply: `2598`
- Unlinked imported legacy profiles after final apply: `0`
- Duplicate linked `cognito_subject` groups: `0`
- Extra Cognito accounts intentionally left unmatched: `1383`

Artifacts:

- [cognito-unmatched-users-2026-03-28.json](./reports/cognito-unmatched-users-2026-03-28.json)
- [cognito-unmatched-users-2026-03-28.csv](./reports/cognito-unmatched-users-2026-03-28.csv)

## Spot Checks

- Visibility normalization:
  archive distribution was `298 public`, `30 private`, `25 sidekicks`
  published distribution is `298 public`, `29 private`, `25 connections`
  the missing private adventure is explained by the single unresolved-author adventure that was not published

- Adventure media:
  published adventures: `352`
  primary `adventure_media` rows: `352`
  non-primary `adventure_media` rows: `0`
  this matches the legacy product reality that `defaultImage` was the authoritative single-image field

- Adventure stats:
  adventures without `adventure_stats`: `0`

- Identity bridge:
  every published legacy profile now maps to Cognito by exact handle, matching the legacy iOS identity model

## Known Non-Blocking Notes

- Full S3 inventory verification is not required to close the migration workstream. It can be treated as a cutover/deployment validation task if needed later.
- A hand-authored rollback strategy is intentionally not required for this workstream. The migration result is reproducible through the stage/transform/publish pipeline and documented source artifacts.

## Conclusion

The migration workstream is complete for planning and implementation purposes in the rebuild program:

- source discovery is complete
- field and identity mapping rules are locked
- migration tooling is implemented and repeatable
- the published dataset reconciles against the archive and documented skip/collapse rules
- the legacy identity bridge is proven and applied
