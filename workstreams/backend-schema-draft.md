# Backend Schema Draft

## Goal

Lock the first relational domain model for the rebuild so backend implementation can start without recreating the legacy Mongo and ACL patterns.

## Scope Of This Draft

- supports slice 1 directly: auth bootstrap, profile bootstrap, feed, map, detail, image delivery
- includes tables needed early for later social and engagement slices so we do not churn the schema immediately after slice 1
- defers non-core operations concerns like analytics, push notifications, and internal admin tooling

## Modeling Principles

- Use internal UUIDs for every primary entity. Do not use legacy usernames as foreign keys.
- Keep Cognito as the external auth provider, but map it into a local `users` row owned by the rebuild backend.
- Separate identity, profile, content, relationships, and media metadata into distinct tables.
- Store content visibility as a stable property on adventures. Do not carry forward `acl[]`.
- Evaluate `connections` access from current relationship state at read time.
- Keep binary media in S3 and keep metadata, moderation state, and ownership in PostgreSQL.
- Treat counters and aggregates as derived data, not as the authoritative write path.

## Canonical Enums

- `adventure_visibility`
  Values: `private`, `connections`, `public`

- `connection_status`
  Values: `pending`, `accepted`, `blocked`

- `adventure_status`
  Values: `draft`, `published`, `archived`

- `media_moderation_status`
  Values: `pending`, `approved`, `rejected`

## Core Tables

### `users`

- `id uuid primary key`
- `cognito_subject text unique not null`
- `handle text unique not null`
- `email text`
- `status text not null default 'active'`
- `created_at timestamptz not null`
- `updated_at timestamptz not null`
- `deleted_at timestamptz null`

Notes:

- `handle` is the public username used for profile routes, author display, and migration from legacy `username`.
- `handle` is stable and non-user-editable in v1.
- `cognito_subject` is the durable auth link. JWT claims should never be trusted as the entire profile record.

### `profiles`

- `user_id uuid primary key references users(id)`
- `display_name text`
- `bio text`
- `home_city text`
- `home_region text`
- `avatar_media_asset_id uuid null references media_assets(id)`
- `cover_media_asset_id uuid null references media_assets(id)`
- `created_at timestamptz not null`
- `updated_at timestamptz not null`

Notes:

- Keep public-facing profile fields here rather than on `users`.
- Legacy `fullName`, `city`, `state`, `profileImage`, and `backgroundImage` map naturally into this table.
- `display_name` is optional, not unique, and may differ from `handle`.

### `connections`

- `id uuid primary key`
- `user_id_low uuid not null references users(id)`
- `user_id_high uuid not null references users(id)`
- `initiated_by_user_id uuid not null references users(id)`
- `status connection_status not null`
- `requested_at timestamptz not null`
- `responded_at timestamptz null`
- `updated_at timestamptz not null`

Constraints:

- unique pair on `(user_id_low, user_id_high)`
- check `user_id_low < user_id_high`
- check `initiated_by_user_id` matches one side of the pair

Notes:

- Store one canonical row per pair of users.
- The API can still expose viewer-oriented states such as `pending_outbound` and `pending_inbound`, but the database should normalize them into a single `pending` status plus `initiated_by_user_id`.
- Legacy `sidekicks` should migrate to `accepted` connection rows.

### `media_assets`

- `id uuid primary key`
- `owner_user_id uuid not null references users(id)`
- `storage_key text unique not null`
- `kind text not null`
- `mime_type text`
- `byte_size integer`
- `width integer`
- `height integer`
- `moderation_status media_moderation_status not null default 'pending'`
- `moderation_reason text null`
- `created_at timestamptz not null`
- `updated_at timestamptz not null`
- `deleted_at timestamptz null`

Notes:

- This replaces the legacy split between S3 object state and the `filenames` moderation queue collection.
- The moderation worker should operate on `media_assets` rows with `moderation_status = 'pending'` rather than a separate filename table.

### `adventures`

- `id uuid primary key`
- `author_user_id uuid not null references users(id)`
- `title text not null`
- `description text null`
- `category_slug text null`
- `visibility adventure_visibility not null default 'private'`
- `status adventure_status not null default 'published'`
- `location geography(Point, 4326) null`
- `place_label text null`
- `created_at timestamptz not null`
- `updated_at timestamptz not null`
- `published_at timestamptz null`
- `archived_at timestamptz null`

Notes:

- `location` uses PostGIS and should back both detail display and map queries.
- `visibility` replaces legacy `access`.
- Published adventures in slice 1 should normally have location data, but drafts can remain incomplete for later creation flows.

### `adventure_media`

- `adventure_id uuid not null references adventures(id)`
- `media_asset_id uuid not null references media_assets(id)`
- `sort_order integer not null`
- `is_primary boolean not null default false`
- `created_at timestamptz not null`

Constraints:

- primary key on `(adventure_id, media_asset_id)`
- unique `(adventure_id, sort_order)`
- partial unique index on `(adventure_id)` where `is_primary = true`

Notes:

- This replaces legacy `images[]` plus `defaultImage`.
- Media ordering and primary-image selection belong here, not in S3 key naming conventions.

### `adventure_favorites`

- `user_id uuid not null references users(id)`
- `adventure_id uuid not null references adventures(id)`
- `created_at timestamptz not null`

Constraints:

- primary key on `(user_id, adventure_id)`

### `adventure_comments`

- `id uuid primary key`
- `adventure_id uuid not null references adventures(id)`
- `author_user_id uuid not null references users(id)`
- `body text not null`
- `created_at timestamptz not null`
- `updated_at timestamptz not null`
- `deleted_at timestamptz null`

Notes:

- Do not denormalize profile image URLs or display names into comment rows.
- Read queries should join the latest profile state for presentation.

### `adventure_ratings`

- `user_id uuid not null references users(id)`
- `adventure_id uuid not null references adventures(id)`
- `score smallint not null`
- `created_at timestamptz not null`
- `updated_at timestamptz not null`

Constraints:

- primary key on `(user_id, adventure_id)`
- check `score between 1 and 5`

Notes:

- This replaces legacy write-time aggregate mutation on `adventures.rating` and `adventures.ratingCount`.

## Phase 3 And 4 Tables

These are not needed to ship slice 1, but should follow naturally from the same model:

- `support_requests`
  For support, bug, and feature messages now grouped in legacy `messages`

- `content_reports`
  For reported adventures, comments, or users

- `account_deletion_requests`
  Optional audit trail if we want a safer delete-account flow than direct destructive execution

## Derived Reads And Projections

- Feed and detail reads can compute author profile data and primary media through joins.
- Favorite counts, comment counts, and rating aggregates should be derived through SQL views or projection tables, not through inline mutation of source rows.
- If feed performance later requires it, add an `adventure_stats` projection table maintained by triggers or background jobs. Do not make it the only source of truth.

## Visibility And Read Rules

### Feed

Return published adventures where one of these is true:

- viewer is the author
- `visibility = 'public'`
- `visibility = 'connections'` and the viewer has an `accepted` connection with the author

Blocked relationships should exclude content in both directions.

### Map

Use the same visibility predicate as feed, then apply bounding-box or radius filters on `location`.

### Profile Browsing

- public profile fields can be returned for signed-in viewers
- authored content on the profile page must still use the adventure visibility rules
- viewers never see another user's `private` adventures

### Detail

Direct lookup by adventure ID must reuse the exact same visibility predicate as list endpoints.

### Media Delivery

Media access should follow the visibility of the owning resource. Do not expose raw bucket paths directly from the client.

## Slice 1 API Implications

This schema supports a clean first API surface:

- `GET /api/me`
- `GET /api/me/profile`
- `PUT /api/me/profile`
- `GET /api/feed`
- `GET /api/map`
- `GET /api/adventures/:id`
- `GET /api/adventures/:id/media`
- `GET /api/profiles/:handle`
- `GET /api/media/:id` or a signed-delivery equivalent

Connections, favorites, comments, and ratings can be added in later slices without changing the core entity boundaries.

## Legacy Mapping Notes

- `profiles.username` -> `users.handle`
- `profiles.fullName` -> `profiles.display_name`
- `profiles.city` and `profiles.state` -> `profiles.home_city` and `profiles.home_region`
- `adventures.access` -> `adventures.visibility`
- `adventures.location` GeoJSON -> `adventures.location geography(Point, 4326)`
- `adventures.images[]` and `defaultImage` -> `media_assets` + `adventure_media`
- `sidekicks` -> `connections`
- `favorites` -> `adventure_favorites`
- `comments` -> `adventure_comments`
- `ratings` -> `adventure_ratings`
- `filenames` moderation queue -> `media_assets.moderation_status = 'pending'`
- `messages` -> `support_requests` or `content_reports` depending on `msgType`

## Decision Summary

The rebuild backend should use normalized relational entities centered on `users`, `profiles`, `connections`, `adventures`, and `media_assets`, with visibility enforced from current relationship state rather than stored ACL snapshots.
