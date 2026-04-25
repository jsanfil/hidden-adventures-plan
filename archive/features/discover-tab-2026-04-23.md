# Feature: Discover Tab

## Summary

Replace the reserved `Saved` tab with a real `Discover` destination that helps users find great adventures through creators, standout posts, and broader regional or destination-oriented discovery.

## Product Intent

- The app is ultimately about finding cool places to explore rather than building a friend network.
- Discover should lean into the social layer only insofar as people act as strong curators of places and adventure taste.
- This feature exists because `Saved` is a utility destination, while `Discover` should become a repeat-use discovery destination that earns a main-tab slot.
- The experience should feel more editorial and inspirational than the current local feed without becoming a generic social app.

## Positioning

- `Home Feed`
  Local adventure stream for what is happening around the viewer now.
- `Map`
  Place-based exploration around a selected location with geographic scope and map interactions.
- `Discover`
  Broader regional and destination-oriented discovery through creators, standout adventures, and mixed people plus adventure search.
- `Profile`
  The viewer's own identity, authored content, saved content, and later profile-based collections.

## Status

- Program status: `Not Started`
- Completion source of truth: this document

## Scope

- new `Discover` main-tab destination
- discovery-home modules, not blank search
- unified search across people and adventures
- creator-led presentation with adventure value still central
- reuse of the existing profile concept when opening creators
- best-first authored-adventure ordering when entering profiles from Discover
- saved-content displacement from main-tab navigation into later profile collections work

## Experience Principles

- Discover is a place-discovery feature first, not a social-network feature.
- People should lead visually because they are the curation lens, but adventures must remain equal in product value.
- The default state should be a discovery home, not a blank search screen.
- Geographic scope should feel broader than the local feed: regional and destination-oriented rather than purely nearby or fully global by default.
- The screen should help users find creators worth browsing and adventures worth opening without introducing DMs, groups, or community mechanics.

## Dependencies

- stable profile foundation
- stable authored-adventure profile reads
- stable sidekick/profile search foundation
- server-owned ranking and discover API support

## Default UX Shape

- Main-tab label is `Discover`.
- The top of the screen is a single search bar that supports both people and adventures.
- The default home should open as curated sections rather than a search-only layout.
- v1 home modules should be ordered as:
  1. `Creators To Explore`
  2. `Rising Explorers`
  3. `Standout Adventures`
  4. `Browse By Category`
  5. `Destination Creators`
- Search results should be grouped into `People` and `Adventures` rather than forced into a single mixed list.
- The first interaction model should bias toward browsing and tapping into creator profiles rather than performing advanced filtering.

## Creator And Profile Behavior

- Creator cards should answer "Why should I browse this person's adventures?" rather than "Why should I connect with this person?"
- Creator cards should include:
  - avatar
  - display name and handle
  - short bio snippet when available
  - home city and region when available
  - adventure count
  - top categories derived from authored adventures
  - preview media or adventure collage
  - a short recommendation reason
- Primary creator-card CTA should be `View Profile`.
- Discover must reuse the same core profile concept already used elsewhere in the app rather than introducing a special Discover-only profile screen.
- When a user opens a creator profile from Discover, authored adventures should default to `best` ordering rather than purely recent ordering.
- Profile entry from Discover should still feel close to the existing `ProfileView` concept, with the main change being emphasis and ordering rather than a separate screen identity.

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- `GET /api/discover/home`
- `GET /api/discover/search`
- optional `sort=recent|best` support on `GET /api/profiles/:handle`
- grouped Discover response types for creators and adventures

## Ranking And Data Strategy

- Discover ranking should be server-owned rather than assembled client-side because the server is closest to the database and ranking inputs.
- Discover must work on day one from the existing V2 dataset and should not depend on newly accumulated Discover-only telemetry before it becomes useful.
- v1 ranking should use existing live data plus derived server-side scoring:
  - published adventure count
  - recency
  - category mix
  - favorite count
  - comment count
  - rating count
  - average rating
  - author location fields
  - optional destination context
- v1 should use light personalization only:
  - destination or selected region context when available
  - viewer home region when available
  - authored-category affinity when it can be derived safely
- New Discover interaction tracking may be added, but it must be additive only and should improve ranking over time rather than gate the first release.
- Do not rely on fixture-only profile social-proof values such as `likes` or `views` unless they become part of a deliberate live server contract.
- Do not require a heavy precomputed recommendation system for v1 if query-time ranking or lightweight derived scoring is sufficient.

## Saved And Favorites Placement

- Replacing the reserved `Saved` tab with `Discover` is a navigation and product-positioning decision, not a statement that saved content is unimportant.
- Saved and favorited adventures should move under later profile-based collection surfaces rather than remain a main-tab destination.
- `Profile Collections` remains the follow-on feature that should absorb saved and authored-content browsing surfaces.
- `Favorites` remains the separate follow-on feature that should own save and unsave mechanics plus favorite-state hydration.

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for discover home, discover search, and profile best-sort reads
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Implementation Defaults

- Tab name is `Discover`.
- Discover becomes the next feature to implement after completed `Sidekicks + Profile Discovery` work.
- `Profile Collections` remains a separate later feature focused on profile-surface collections.
- `Favorites` remains a separate later feature focused on save and unsave mechanics plus favorite-state hydration.
- Discover v1 uses existing live signals plus server-derived ranking:
  - published adventure count
  - recency
  - category mix
  - favorite count
  - comment count
  - rating count
  - average rating
  - author location fields
  - optional destination context
- Any new Discover interaction tracking is additive only and must not be required for launch quality.

## Non-Goals

- Do not turn Discover into a DM, inbox, or chat surface.
- Do not optimize the screen around friendship mechanics, interest groups, or community management.
- Do not make Discover a clone of the local feed or the map experience.
- Do not rank the entire surface as a pure popularity board driven only by post count.
- Do not introduce a second profile concept that competes with the existing profile flow.

## Notes

- Discover is about place discovery, not DMs, groups, or friend-network mechanics.
- People lead visually because they are curators of places rather than the primary product destination.
- Saved and favorited items are no longer a main-tab destination and should land under later profile-based collection surfaces.
- Discover ranking should work immediately from the existing V2 dataset, with any new interaction tracking improving the surface over time rather than gating launch.
