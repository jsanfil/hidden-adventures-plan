# Visibility Model Recommendation

## Goal

Replace the legacy `access + acl[] + sidekicks` visibility behavior with a clearer policy model that preserves the product's selective-sharing value without carrying forward document-mutation coupling.

## Legacy Problem

The legacy product uses:

- `access` on adventures with values like `private`, `sidekicks`, and `public`
- `acl[]` on adventures to store usernames who may view shared content
- sidekick add/remove flows that mutate every authored adventure's `acl[]`

This causes several issues:

- content visibility is coupled to historical username snapshots
- relationship changes require bulk mutation of previously created records
- the UI concept and the data model are tightly entangled
- the model is difficult to express cleanly in a relational backend

## Recommendation

Use explicit visibility policies on content and evaluate access from current relationship state at read time.

### Canonical visibility levels

- `private`
  Meaning: only the author can view the adventure

- `connections`
  Meaning: the author and approved connections can view the adventure

- `public`
  Meaning: any signed-in user can view the adventure

## Social model dependency

Visibility should depend on a modern connection model rather than legacy one-way sidekick rows.

Recommended relationship states:

- `pending_outbound`
- `pending_inbound`
- `accepted`
- `blocked`

Only `accepted` relationships should grant access to `connections` content.

## Access rules

### Feed

- authors always see their own content regardless of visibility
- `private` content appears only for the author
- `connections` content appears for the author and users with an accepted connection to the author
- `public` content appears for all signed-in viewers

### Map

- same core visibility rules as feed
- map filtering should apply after visibility evaluation, not instead of it

### Profile browsing

- viewers can always see the author's `public` adventures
- viewers can see `connections` adventures only when the relationship is `accepted`
- viewers never see another user's `private` adventures

### Detail routes

- detail access should be authorized by the same policy engine used for list queries
- do not expose content by direct ID lookup if list-level visibility would deny it

## Data model shape

Recommended relational shape:

- `adventures.visibility`
  Enum: `private | connections | public`

- `connections`
  Fields: `requester_user_id`, `target_user_id`, `status`, timestamps

Optional future extension:

- `adventure_visibility_exceptions`
  Use only if we later need explicit per-user sharing beyond the three-level model

Do not introduce exceptions in phase 1 unless a concrete product requirement appears.

## Why this is better

- preserves the old product's three sharing intents
- removes `acl[]` mutation from create/add/remove-connection flows
- makes visibility a stable property of content
- makes connection state a stable property of the relationship graph
- maps cleanly to SQL joins and policy checks
- simplifies client copy and settings UX

## UX implications

Recommended user-facing labels:

- `Only Me`
- `Connections`
- `Public`

Guidance:

- avoid exposing raw policy concepts like ACL or sidekick lists in the client
- explain `Connections` in plain language at creation time
- show visibility state clearly on authored content
- keep viewer mental models simple: who can see this now, not who is in a stored list

## Migration interpretation

Legacy `sidekicks` should be treated as source data for seeding accepted relationships.

Legacy adventure visibility mapping:

- `private` -> `private`
- `public` -> `public`
- `sidekicks` -> `connections`

Legacy `acl[]` should not be preserved as the long-term authorization mechanism.

During migration:

- derive access from migrated relationships where possible
- treat `acl[]` as a migration aid and verification input
- do not design new APIs or UI around it

## API implications

Recommended patterns:

- content create/update accepts `visibility`
- list/detail endpoints evaluate visibility server-side
- connection endpoints own relationship state transitions
- no content endpoint should require callers to pass allowed usernames

## Open questions

- Should `connections` require mutual acceptance or be modeled as follower/following with a separate "trusted" state?
- Should public profile fields and public content visibility be controlled separately?
- Do we need a moderator/admin override path in phase 1, or only in later operations work?

## Decision summary

Adopt `private`, `connections`, and `public` as the rebuild visibility model, backed by current relationship state rather than stored per-adventure ACL usernames.
