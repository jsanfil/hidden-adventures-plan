# Legacy To New Mapping

## Goal

Define how the legacy Mongo archive maps into the rebuild relational model so migration tooling can be implemented repeatably against the real archive.

## Source Inputs

- Legacy archive: `migration/archives/legacy-mongodb-backup-2026-03-01.archive`
- Archive profile: [archive-profile.md](./archive-profile.md)
- Legacy inventory: [legacy-inventory.md](./legacy-inventory.md)
- Cognito linking findings: [cognito-account-linking-findings.md](./cognito-account-linking-findings.md)
- Target relational model: [backend-schema-draft.md](../workstreams/backend-schema-draft.md)

## Migration Principles

- Use the Mongo archive as the source of truth for imported data, not inferred controller behavior alone.
- Preserve user-visible state where possible, even when legacy modeling was denormalized.
- Do not carry forward legacy implementation artifacts such as `acl[]`, username foreign keys, or document-coupled aggregate mutation.
- Skip or quarantine invalid references instead of importing broken rows silently.
- Keep an import audit artifact that records every skipped or transformed legacy record.

## Pre-Migration Constraints

### Identity gap

The archive is keyed by legacy usernames, but the rebuild schema is keyed by UUID user IDs and expects Cognito-backed identity.

Required migration stance:

- import users by legacy `username` into `users.handle`
- generate new UUIDs for rebuild primary keys
- treat Cognito linkage as a post-import identity binding step

Practical implication:

- `users.cognito_subject` cannot be fully populated from this archive alone
- either the rebuild schema must allow `cognito_subject` to be null during import, or the import must stage users until Cognito linkage data is available

This is the main open architecture constraint exposed by the archive.

### Account linking strategy

Legacy code paths used Cognito username as the primary authenticated identity key, not email, and live-pool validation confirmed that the published legacy profile set maps cleanly by exact handle.

Recommended one-time linking order:

1. exact Cognito `Username` -> exact imported `users.handle`
2. skip everything else during bulk migration
3. reserve verified-email matching for the runtime legacy-account claim flow, not the bulk link job

Rules:

- do not bulk auto-link by email
- do not invent placeholder Cognito subjects
- once linked, persist the real Cognito `sub` into `users.cognito_subject`
- do not create `public.users` rows for unmatched Cognito accounts that never had a legacy profile

## Collection Mapping Summary

| Legacy Source | New Target | Notes |
| --- | --- | --- |
| `profiles` | `users`, `profiles`, optional `media_assets` | identity and public profile bootstrap |
| `adventures` | `adventures`, `media_assets`, `adventure_media`, rating projection | core content import |
| `sidekicks` | `connections` | dedupe into one canonical pair row |
| `favorites` | `adventure_favorites` | import only when both user and adventure resolve |
| `comments` | `adventure_comments` | import only when both user and adventure resolve |
| `ratings` | no per-user row import from this archive | preserve aggregate rating state only |
| `messages` | `support_requests` or `content_reports` later | no rows present in this archive |
| `filenames` | `media_assets.moderation_status` later | no rows present in this archive |

## Canonical Key Strategy

Create stable import lookup maps before loading child tables:

- `legacy_username -> users.id`
- `legacy_adventure_id -> adventures.id`
- `legacy_media_key -> media_assets.id`

Import tooling should persist these maps in staging artifacts so reruns are deterministic.

## Field-Level Mapping

### `profiles` -> `users` + `profiles`

Source fields:

- `username`
- `email`
- `fullName`
- `city`
- `state`
- `profileImage`
- `backgroundImage`
- `adventureCount`
- timestamps

Target mapping:

| Legacy Field | New Field | Rule |
| --- | --- | --- |
| `username` | `users.handle` | required; preserve exact case for initial import unless handle normalization rules are defined separately |
| `email` | `users.email` | nullable |
| archive presence | `users.status` | import as `active` unless later moderation/deletion evidence exists |
| `fullName` | `profiles.display_name` | nullable |
| `city` | `profiles.home_city` | nullable |
| `state` | `profiles.home_region` | nullable |
| `profileImage` | `profiles.avatar_media_asset_id` | create linked `media_assets` row when key exists |
| `backgroundImage` | `profiles.cover_media_asset_id` | create linked `media_assets` row when key exists |
| `createdAt` | `users.created_at`, `profiles.created_at` | preserve timestamp |
| `updatedAt` | `users.updated_at`, `profiles.updated_at` | preserve timestamp |

Notes:

- `adventureCount` should not become a persisted source-of-truth field in the rebuild database.
- Use it only as a reconciliation check against imported adventure ownership counts.

### `adventures` -> `adventures`

Source fields:

- `_id`
- `name`
- `desc`
- `author`
- `access`
- `defaultImage`
- `category`
- `images[]`
- `location`
- `rating`
- `ratingCount`
- `acl[]`
- timestamps

Target mapping:

| Legacy Field | New Field | Rule |
| --- | --- | --- |
| `_id` | import map only | keep in audit map; do not reuse as primary key |
| `author` | `adventures.author_user_id` | resolve through `legacy_username -> users.id` |
| `name` | `adventures.title` | required |
| `desc` | `adventures.description` | primary description field for phase 1 |
| `category` | `adventures.category_slug` | normalize through category mapping table below |
| `access` | `adventures.visibility` | normalize through visibility mapping below |
| archive state | `adventures.status` | import as `published` |
| `location.coordinates` | `adventures.location` | convert GeoJSON point to PostGIS geography point |
| null | `adventures.place_label` | leave null unless later reverse-geocoding is desired |
| `createdAt` | `adventures.created_at`, `published_at` | preserve timestamp |
| `updatedAt` | `adventures.updated_at` | preserve timestamp |

Notes:

- Every adventure in this archive has location data.
- Every adventure in this archive has `defaultImage`.
- The shipped legacy product only used `defaultImage` for adventure media. `images[]` was never fully implemented and should not be treated as authoritative media inventory.

### `adventures.defaultImage` -> `media_assets` + `adventure_media`

Primary import rule:

- create one `media_assets` row for `defaultImage` when present
- set `owner_user_id` to the adventure author
- set `storage_key` to the legacy image key exactly as stored
- set `kind` to `adventure_image`
- set `moderation_status` to `approved` for imported legacy media unless a later moderation source says otherwise

Then:

- create one `adventure_media` row linking the imported media asset to the adventure
- set `sort_order = 0`
- set `is_primary = true`

Secondary rule:

- do not create additional `adventure_media` rows from the empty `images[]` arrays in this archive
- do not treat the blank `images[]` arrays as a data-quality issue because multi-image support was not actually implemented in the legacy app
- if a later migration phase introduces more complete media manifests, those can extend the imported media set

### `sidekicks` -> `connections`

Source fields:

- `username`
- `sidekickName`
- `sidekickImage`
- timestamps

Target mapping:

| Legacy Field | New Field | Rule |
| --- | --- | --- |
| `username`, `sidekickName` | `user_id_low`, `user_id_high` | resolve both usernames to imported users, sort pair canonically |
| legacy row presence | `status` | import as `accepted` |
| inferred initiator | `initiated_by_user_id` | use the `username` side of the original row |
| `createdAt` | `requested_at` | preserve timestamp |
| `updatedAt` | `responded_at`, `updated_at` | preserve timestamp |

Deduping rules:

- multiple rows for the same pair collapse into one canonical connection
- if both directions exist, keep the earliest `createdAt` as `requested_at`
- if only one direction exists, still import one `accepted` connection row

Rationale:

- the rebuild uses mutual `connections`, not one-way sidekick lists
- legacy sidekick rows are the closest available source for seeding accepted relationships

### `favorites` -> `adventure_favorites`

Source fields:

- `username`
- `adventureID`
- timestamps

Target mapping:

| Legacy Field | New Field | Rule |
| --- | --- | --- |
| `username` | `adventure_favorites.user_id` | resolve through imported user map |
| `adventureID` | `adventure_favorites.adventure_id` | resolve through imported adventure map |
| `createdAt` | `adventure_favorites.created_at` | preserve timestamp when present |

Import rule:

- import only when both user and adventure resolve
- delete unresolved rows during migration rather than preserving dangling favorites
- record deleted rows in an import audit report

Archive note:

- this archive contains `61` favorites pointing at missing adventures
- this archive contains `19` favorites whose usernames do not resolve to a profile

### `comments` -> `adventure_comments`

Source fields:

- `username`
- `adventureID`
- `text`
- `usernameImage`
- timestamps

Target mapping:

| Legacy Field | New Field | Rule |
| --- | --- | --- |
| `_id` | audit map only | do not reuse as primary key |
| `username` | `adventure_comments.author_user_id` | resolve through imported user map |
| `adventureID` | `adventure_comments.adventure_id` | resolve through imported adventure map |
| `text` | `adventure_comments.body` | required |
| `createdAt` | `adventure_comments.created_at` | preserve timestamp |
| `updatedAt` | `adventure_comments.updated_at` | preserve timestamp |
| null | `adventure_comments.deleted_at` | leave null |

Notes:

- ignore `usernameImage` during import; the rebuild should derive avatar display from the current profile record
- delete unresolved rows during migration rather than preserving dangling comments
- record deleted rows in an import audit report

### `ratings` -> aggregate rating state only

Archive reality:

- there is no `ratings` collection in this archive
- adventure rows still contain `rating` and `ratingCount`
- legacy displayed rating was `rating / ratingCount`

Migration rule:

- do not synthesize `adventure_ratings` rows from aggregate data
- preserve rating display state through an import-time projection

Recommended target:

- load legacy `rating` as `legacy_rating_sum`
- load legacy `ratingCount` as `legacy_rating_count`
- expose average rating to the app as `legacy_rating_sum / legacy_rating_count` when count is non-zero

Implementation note:

- this can live in a migration-side staging table or an `adventure_stats` projection table
- it should not be modeled as fake per-user ratings

### `messages` and `filenames`

Archive reality:

- both collections exist but contain zero rows in this archive

Migration rule:

- no row import in the initial migration
- keep table structures ready for later imports if another archive or production source provides records

## Visibility Mapping

| Legacy `access` | New `visibility` |
| --- | --- |
| `Private` | `private` |
| `Sidekicks` | `connections` |
| `Public` | `public` |

Notes:

- preserve author visibility for all imported adventures
- do not import `acl[]` as the long-term authorization model
- keep `acl[]` only as an audit aid when validating `connections` visibility migration

Special case:

- `4` `Sidekicks` adventures in this archive have no ACL payload
- access conversion should still map them to `connections`, but validation should flag them for manual review if connection seeding does not explain expected visibility

## Category Normalization

The rebuild should use a fixed eight-category enum. These are code-safe enum values, not dashed slugs. UI should always render the friendly title, not the raw enum value.

| Enum Value | UI Title | Legacy Categories Mapped |
| --- | --- | --- |
| `viewpoints` | Viewpoints | `Viewpoint` |
| `trails` | Trails | `Trail` |
| `water_spots` | Water Spots | `Beach_Cove`, `Creek_Rivers`, `SwimmingHole`, `RopeSwing`, `Fishing` |
| `food_drink` | Food & Drink | `Restaurant`, `Cafe`, `Bar`, `LiveMusic` |
| `abandoned_places` | Abandoned Places | `Abandoned` |
| `caves` | Caves | `Cave` |
| `nature_escapes` | Nature Escapes | `Forest`, `Desert` |
| `roadside_stops` | Roadside Stops | `road`, `Bridge` |

Why this normalization:

- it preserves the most popular legacy categories as distinct top-level choices
- it collapses low-volume legacy strings into broader labels that are easier to understand in product UI
- it covers the full original category spectrum without introducing an `other` bucket into the fixed app taxonomy

Implementation notes:

- backend should store the enum-style identifier in `adventures.category_slug` until the column is renamed later
- iOS should mirror the same eight values as a Swift enum with a computed display title
- import tooling should keep the raw legacy category in an audit artifact for traceability
- if later legacy sources introduce unknown categories, quarantine them for review instead of auto-mapping to a ninth catch-all bucket

## Data Quality Rules

### Required skips and quarantine

Do not import child rows when required parents are missing:

- favorites with missing user or adventure; delete these during migration
- comments with missing user or adventure; delete these during migration
- sidekick rows where either user cannot be resolved
- adventures where author cannot be resolved

All skipped or deleted rows should be written to an import reconciliation artifact with:

- source collection
- source legacy ID or natural key
- reason skipped
- raw payload reference

### Preserve but normalize

Normalize during import:

- category strings to slugs
- visibility values to lowercase enum values
- timestamps to UTC
- usernames into UUID foreign keys

Do not normalize away:

- legacy image storage keys
- legacy created/updated timestamps

## Reconciliation Targets

Initial reconciliation should verify:

- profile rows imported versus archive profile count
- adventure rows imported versus archive adventure count
- accepted connections imported versus deduped sidekick pair count
- favorite rows imported plus favorite rows quarantined equals archive favorite count
- comment rows imported plus comment rows quarantined equals archive comment count
- category distribution after normalization matches archive distribution by mapping table
- visibility distribution after normalization matches legacy access distribution
- computed displayed rating for imported adventures matches `rating / ratingCount` from the archive

## Open Decisions

- whether to temporarily allow `users.cognito_subject` to be null during import
- whether imported aggregate ratings should live in a staging table or a durable `adventure_stats` projection
- whether `roadside-stop` is the final product label for legacy `road`
- whether imported legacy media should default to `approved` or to a separate `grandfathered` moderation state

## Decision Summary

Import legacy profiles, adventures, sidekicks, favorites, and comments directly from the archive into normalized relational tables, preserve media and rating display state from aggregate fields, and quarantine unresolved references instead of inventing missing parent records.
