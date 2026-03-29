# PostgreSQL Import Flow

## Goal

Define a repeatable import pipeline that converts the legacy Mongo archive into the rebuild PostgreSQL model with staging, validation, audit logging, and safe publish semantics.

## Inputs

- Legacy archive: `migration/archives/legacy-mongodb-backup-2026-03-01.archive`
- Archive profile: [archive-profile.md](./archive-profile.md)
- Legacy mapping rules: [legacy-to-new-mapping.md](./legacy-to-new-mapping.md)
- Cognito linking findings: [cognito-account-linking-findings.md](./cognito-account-linking-findings.md)
- Target schema: [backend-schema-draft.md](../workstreams/backend-schema-draft.md)

## Recommended Strategy

Use a three-layer migration flow:

1. archive extraction into raw migration artifacts
2. PostgreSQL staging and normalization
3. validated publish into application tables

This is better than writing directly into app tables because it:

- makes dry runs repeatable
- preserves raw source payloads for debugging
- gives us explicit quarantine and deletion reporting
- lets us validate counts and relationships before publish

## Recommended PostgreSQL Schemas

### `migration_meta`

Purpose:

- track import runs
- track run status
- store audit rows and reconciliation metrics

Recommended tables:

- `import_runs`
  Fields: `id`, `started_at`, `completed_at`, `archive_path`, `archive_checksum`, `status`, `notes`

- `import_metrics`
  Fields: `run_id`, `metric_name`, `metric_value`, `details_json`

- `import_audit`
  Fields: `run_id`, `source_collection`, `source_key`, `action`, `reason`, `payload_json`

### `migration_stage`

Purpose:

- store raw extracted records exactly as imported from the archive

Recommended tables:

- `profiles_raw`
- `adventures_raw`
- `sidekicks_raw`
- `favorites_raw`
- `comments_raw`

Common fields:

- `run_id`
- `source_key`
- `payload_json jsonb`
- `loaded_at`

### `migration_work`

Purpose:

- store normalized, relationally-shaped records before publishing to app tables

Recommended tables:

- `users_work`
- `profiles_work`
- `media_assets_work`
- `adventures_work`
- `connections_work`
- `adventure_favorites_work`
- `adventure_comments_work`
- `adventure_rating_projection_work`
- `import_maps`

`import_maps` should store deterministic lookup records:

- `map_type`
- `legacy_key`
- `new_id`
- `run_id`

Example map types:

- `legacy_username_to_user_id`
- `legacy_adventure_id_to_adventure_id`
- `legacy_media_key_to_media_asset_id`

## Run Modes

### Dry run

Dry run should:

- extract the archive
- load stage tables
- build normalized work tables
- generate audit rows and reconciliation metrics
- stop before writing to application tables

Dry run should not:

- mutate `public` application tables
- require Cognito subjects to be present

### Publish run

Publish run should:

- require a successful dry run against the same archive checksum
- truncate or isolate prior imported target rows in a controlled way
- write application-table rows inside a transaction boundary where practical
- record publish metrics and final status in `migration_meta.import_runs`

## Archive Extraction Step

Recommended process:

1. Compute archive checksum and create a new `import_runs` row.
2. Parse the archive into collection-specific NDJSON or CSV artifacts.
3. Save those extracted artifacts under a run directory in `tmp` or a migration output directory that is not committed.
4. Load each collection artifact into `migration_stage.*_raw`.

Recommended implementation note:

- reuse [profile_mongo_archive.py](../scripts/profile_mongo_archive.py) as the archive parser foundation
- add a sibling extractor script later rather than introducing a separate restore dependency

## Load Order

Normalized import should happen in this order:

1. `profiles` -> `users_work`
2. `profiles` -> `profiles_work`
3. profile and cover image keys -> `media_assets_work`
4. `adventures` -> `adventures_work`
5. adventure `defaultImage` keys -> `media_assets_work`
6. adventure primary-image links -> `adventure_media` publish set
7. `sidekicks` -> `connections_work`
8. `favorites` -> `adventure_favorites_work`
9. `comments` -> `adventure_comments_work`
10. adventure aggregate ratings -> `adventure_rating_projection_work`

Rationale:

- users and their ID maps must exist before child records can resolve
- media keys should resolve before profile and adventure foreign keys are published
- favorites and comments depend on both user and adventure maps

## Identity Strategy

### Recommendation

For migration runs, allow imported users to exist before Cognito subject binding.

Recommended implementation options:

- preferred: make `users.cognito_subject` nullable until account binding is completed
- fallback: publish imported users into a staging-owned user table and only promote them after Cognito linkage

Recommendation:

- choose the nullable `cognito_subject` path unless there is a strong security or product reason not to

Why:

- the archive only contains legacy usernames and profile data
- blocking the import on Cognito linkage would slow every dry run
- the rebuild needs deterministic IDs now, not perfect auth binding on day one of migration tooling

### Linking order

When binding imported users to Cognito accounts later, use:

1. exact Cognito `Username` -> exact `users.handle`
2. skip everything else during the bulk link job
3. use verified-email matching only in the runtime legacy-account claim flow

Why this order:

- legacy client and server code both treated Cognito username as the primary identity bridge
- live-pool validation showed the published legacy profile set maps completely by exact handle
- the Cognito pool contains extra abandoned and duplicate accounts that should not be bulk-linked into app identity

Implementation recommendation:

- keep a `migration_meta.import_audit` action for `linked_by_username` and `skipped_no_legacy_profile_match`
- record the Cognito `sub`, Cognito username, and matched imported user ID for every linkage event
- persist a saved list of unmatched Cognito accounts for possible later cleanup rather than auto-deleting them during the link job

## Per-Entity Publish Rules

### Users and profiles

- publish all valid `users_work` and `profiles_work` rows
- preserve imported timestamps
- do not publish `adventureCount` as a stored field

### Media

- publish one `media_assets` row per imported `profileImage`, `backgroundImage`, and `defaultImage`
- preserve `storage_key` exactly
- mark imported legacy assets as `approved` unless later moderation policy requires a dedicated grandfathered status

### Adventures

- publish all adventures whose author resolved successfully
- publish `visibility` from normalized access mapping
- publish `category_slug` from normalized category mapping

### Connections

- publish deduped canonical rows only
- import as `accepted`
- keep duplicate and unresolved source rows in `import_audit`

### Favorites and comments

- publish only resolved rows
- delete unresolved rows during migration cleanup
- record each deleted orphan in `import_audit`

### Rating projection

- do not publish synthetic per-user rating rows
- publish aggregate display state through a projection table or derived stats table
- preserve:
  - `legacy_rating_sum`
  - `legacy_rating_count`
  - derived `average_rating`

## Reconciliation Gates

A dry run is considered acceptable only if it records:

- imported profiles plus skipped profiles equals archive profile count
- imported adventures plus skipped adventures equals archive adventure count
- imported favorites plus deleted orphan favorites equals archive favorite count
- imported comments plus deleted orphan comments equals archive comment count
- normalized visibility distribution matches legacy access distribution
- normalized category distribution matches mapped legacy category distribution
- profile `adventureCount` mismatches remain within expected tolerance, ideally zero
- all imported adventures retain their `defaultImage` mapping
- all imported average ratings equal `rating / ratingCount` from the archive

## Publish Mechanics

Recommended publish shape:

1. begin import run
2. load stage tables
3. populate work tables
4. run reconciliation queries
5. if reconciliation fails, mark run failed and stop
6. if reconciliation passes, publish to application tables in dependency order
7. refresh derived projections
8. mark run published

For early development:

- publish into a disposable local database first
- avoid mixing migration publish logic with production request-serving code

## Rollback Strategy

The first migration tooling should support rollback by replacement, not by piecemeal undo.

Recommended rollback options:

- preferred local/staging path: drop and recreate migrated app tables from schema migrations, then rerun import
- production-safe later path: publish into a fresh schema or fresh database and swap over only after validation

Do not rely on hand-authored row-by-row rollback scripts for the first version.

## Output Artifacts Per Run

Each run should produce:

- one `import_runs` row
- one archive checksum
- extracted raw collection artifacts
- populated `migration_stage` and `migration_work` rows
- import audit rows for skipped, deleted, deduped, or transformed records
- reconciliation metrics
- a human-readable summary report

## Immediate Implementation Tasks

- extend the archive parser into a collection extractor
- create SQL migrations for `migration_meta`, `migration_stage`, and `migration_work`
- decide the nullable `users.cognito_subject` path
- define the one-time Cognito account-linking job using username-first matching
- implement the dry-run loader for `profiles` and `adventures` first
- add reconciliation SQL for counts, category distribution, visibility distribution, and orphan deletion counts

## Decision Summary

Use a staged PostgreSQL import pipeline with raw archive capture, normalized work tables, deterministic ID maps, reconciliation gates, and audited publish steps. Delete orphaned favorites and comments during migration, treat `defaultImage` as the full legacy adventure media model, and preserve only aggregate rating state from the archive.
