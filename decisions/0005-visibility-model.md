# ADR-0005: Visibility Based On Policy And Sidekick State

## Status

Accepted

## Context

The legacy product uses a combination of adventure `access`, per-adventure `acl[]` usernames, and sidekick mutations to control visibility. That model preserves the original product behavior, but it tightly couples content access to denormalized username lists and bulk record mutation. The rebuild is moving to a relational backend and a modernized social model, so visibility must become easier to reason about in both product and schema terms.

## Decision

Adopt a three-level product visibility model for adventures: `private`, `sidekicks`, and `public`. Evaluate access from the adventure's visibility plus the current relationship state between viewer and author. Do not use per-adventure ACL username arrays as the primary authorization mechanism in the rebuild. In the current server implementation, `sidekicks` remains stored as `connections`.

## Consequences

- Visibility becomes easier to explain in product copy and easier to implement in SQL and API policy checks.
- Relationship changes no longer require bulk mutation of previously created adventures.
- Legacy `sidekicks` and `acl[]` data become migration inputs rather than long-term domain shapes.

## Links

- [workstreams/visibility-model.md](../workstreams/visibility-model.md)
- [workstreams/product-ux.md](../workstreams/product-ux.md)
- [workstreams/backend-platform.md](../workstreams/backend-platform.md)
- [migration/legacy-inventory.md](../migration/legacy-inventory.md)
