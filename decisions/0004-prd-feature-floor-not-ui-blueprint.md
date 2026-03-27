# ADR-0004: PRD As Feature Floor, Not UI Blueprint

## Status

Accepted

## Context

The rebuild now has a reverse-engineered PRD from the original Hidden Adventures product. That document is useful because it captures the existing shipped behavior across the iOS app, server, and operations tooling. It is also risky because it could be misread as a requirement to recreate the current app exactly, including outdated navigation, social naming, and legacy implementation artifacts.

## Decision

Use the original PRD as the baseline feature floor for the modernization, while explicitly rejecting screen-for-screen recreation of the legacy UX. The rebuild should preserve essential user capabilities and operational flows, but redesign navigation, information architecture, visibility UX, social UX, and backend architecture for a modern product.

## Consequences

- The team can safely preserve important behaviors without inheriting legacy UI decisions by default.
- Product, iOS, and backend workstreams can modernize aggressively as long as they preserve the agreed feature floor.
- Legacy implementation details such as MongoDB document shape, ACL arrays, ignored token expiration, and disabled SSL evaluation are migration inputs and risk notes, not rebuild targets.

## Links

- [migration/prd-modernization-baseline.md](../migration/prd-modernization-baseline.md)
- [workstreams/product-ux.md](../workstreams/product-ux.md)
- [master-plan.md](../master-plan.md)
