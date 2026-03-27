# PRD Modernization Baseline

## Source

- Original PRD reviewed from `/Users/josephsanfilippo/Documents/projects/hidden.adventures/output/pdf/hidden-adventures-suite-prd.pdf`
- Review date: 2026-03-26

## Intent

Use the reverse-engineered PRD as the baseline feature floor for the rebuild, while explicitly avoiding a screen-for-screen recreation of the legacy app.

The PRD is valuable for:

- confirming the current product surface area
- identifying cross-entity behavior that must not be dropped accidentally
- preserving release-slice relevance for feed, map, detail, creation, profile, social, support, and account-management flows

The PRD should not be treated as:

- a mandate to preserve legacy storyboard structure
- a mandate to preserve legacy information architecture
- a mandate to preserve legacy copy, layout, iconography, or interaction patterns
- a mandate to preserve backend implementation details that are only artifacts of the old stack

## Feature Floor To Preserve

### Discovery and core content

- nearby feed of adventures
- map-based discovery
- full adventure detail view
- category-based exploration
- favorites
- comments
- ratings
- directions / map handoff

### Content creation

- create adventure with title, image, description, location, category, and visibility
- image upload flow
- location selection workflow
- visibility / sharing controls

### Identity and profile

- Cognito-backed sign-in, sign-up, confirmation, and password recovery
- first-run profile creation
- profile editing
- current-user profile view
- authored posts and favorites on profile

### Social layer

- social graph concept currently called sidekicks
- searchable profile discovery
- relationship add/remove flow
- viewing another user's visible adventures

### Support and account management

- contact support
- report content
- legal pages
- logout
- delete account

## Modernization Guidance

### Keep the capability, redesign the experience

- Preserve the feed, map, detail, create, profile, and social capabilities, but redesign their navigation and interaction model around modern SwiftUI patterns.
- Replace the legacy tab-plus-storyboard feel with a more intentional app shell, stronger hierarchy, and cleaner transitions between browse, create, and profile areas.
- Keep map and feed as complementary discovery modes, but design them as parts of one coherent exploration system instead of disconnected tabs.

### Simplify social and visibility

- Treat sidekicks as a legacy social concept that may evolve into a cleaner connection model.
- Preserve the practical product need behind it: selective sharing, trusted-network discovery, and visible profile relationships.
- Rework visibility rules into a clearer policy model instead of copying ACL-shaped UX directly into the new client.

### Modernize content quality and trust

- Preserve comments, ratings, favorites, and reporting, but make trust-and-safety surfaces feel first-class instead of bolted on.
- Keep support and delete-account flows visible and reliable.
- Preserve image moderation intent, but do not assume the old queueing implementation is the long-term solution.

### Do not preserve legacy constraints as product requirements

- MongoDB collections and denormalized document patterns are legacy implementation details, not rebuild requirements.
- The old JWT expiration bypass, disabled SSL evaluation, and other unsafe behaviors are migration risks to eliminate, not compatibility targets.
- The old category taxonomy is useful as seed content, but can be refined if the new IA stays compatible with the feature floor.

## Key Legacy Behaviors Worth Re-expressing In New Architecture

- feed visibility combines ownership, visibility mode, relationship state, and geography
- adding or removing a social connection changes who can see previously created content
- profile images propagate into social and comment surfaces
- content deletion has secondary effects on favorites and ratings
- account deletion touches both application data and Cognito identity
- support, reports, and moderation are part of the shipped product, not afterthoughts

## Recommended Rebuild Interpretation

### Slice 1 baseline

- auth bootstrap
- profile bootstrap
- nearby feed
- map discovery
- adventure detail
- image delivery

### Preserve but redesign later slices

- create/edit adventure
- uploads and location/category controls
- visibility controls
- social graph and profile collections
- comments and ratings polish
- moderation and support workflows

## Open Product Questions

- Should "sidekicks" remain a user-facing term, or should the concept be renamed while preserving its underlying access semantics?
- Should feed and map remain separate top-level tabs, or become two views within one discovery area?
- Which parts of the category tree are true user value versus legacy taxonomy drift?
- How much of the profile surface should stay public versus relationship-gated in the rebuild?

## Outcome

The PRD is now approved as inspiration and feature-floor input for modernization, not as a blueprint for recreating the legacy app exactly.
