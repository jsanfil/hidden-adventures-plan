# Feature: Discover Tab

## Summary

Replace the reserved `Saved` tab with a real `Discover` destination that helps users browse adventurers and adventures using data the rebuild already stores and exposes cleanly.

## Product Intent

- The app is still about finding cool places through people and content, but Discover v1 should stay grounded in straightforward public profile and adventure data.
- This feature exists because `Saved` is a utility destination, while `Discover` should become a repeat-use browsing destination that earns a main-tab slot.
- The experience should feel broader than the local feed and less map-driven than Explore, without pretending the app already has a recommendation system or a second place-search surface.

## Positioning

- `Home Feed`
  Local, location-driven stream of what is happening around the viewer now.
- `Map`
  Place-based exploration around a selected location with geographic scope.
- `Discover`
  Broader public browsing across adventurers and adventures, plus grouped people and adventure text search.
- `Profile`
  The viewer's own identity, authored content, saved content later, and account-centered surfaces.

## Status

- Program status: `Not Started`
- Completion source of truth: this document

## Scope

- new `Discover` main-tab destination
- discovery-home modules, not blank search
- unified text search across people and adventures
- adventurers and adventures both visible on the home
- reuse of the existing profile concept when opening adventurers
- no Discover-only profile surface
- no Discover-specific authored-adventure ordering change in v1
- no geographic query expansion inside Discover search

## Experience Principles

- Keep Discover browse-first.
- Keep the data story honest.
- Keep adventurers present, but do not overclaim why an adventurer is worth following.
- Keep adventures central in product value.
- Keep Discover distinct from feed and map by being broader and non-local by default.
- Avoid heavy filtering, recommendation framing, social-network mechanics, and vague place-search behavior.

## Dependencies

- stable profile foundation
- stable authored-adventure profile reads
- stable profile search foundation
- stable public adventure read models
- server support for Discover home and grouped search

## Default UX Shape

- Main-tab label is `Discover`.
- The top of the screen is a single search bar.
- The default home opens to two modules in this order:
  1. `Explore Adventurers`
  2. `Popular Adventures`
- Search results are grouped into `People` and `Adventures`.
- Search results render in one continuous vertical scroll.
- The first interaction model favors browsing and tapping into profiles or adventure detail, not advanced filtering.

## Home Module Definitions

- `Explore Adventurers`
  - Source only adventurers with at least one public published adventure.
  - Order by public published adventure count descending, then most recent public published adventure descending.
  - Card contents:
    - avatar when present
    - display name or handle
    - handle
    - home city and region when present
    - public adventure count
    - top 1-2 adventure categories
    - preview media from public authored adventures
  - Do not require bio snippets, recommendation reasons, "featured" explanations, or destination claims.

- `Popular Adventures`
  - Source public published adventures only.
  - Order by favorite count descending, then comment count descending, then average rating descending, then publish recency descending.
  - Use existing derived stats or projections only; do not require new telemetry or recommendation infrastructure.
  - Card contents:
    - primary image
    - title
    - author identity
    - category
    - place label or location text when available
    - rating display only if the current read model already exposes it cleanly

## Adventurer And Profile Behavior

- Adventurer cards should answer "who has public adventures worth browsing?" in a simple, factual way.
- Discover must reuse the same core profile concept already used elsewhere in the app.
- Opening an adventurer from Discover should keep the current profile adventure ordering behavior.
- Do not introduce a new `best` sort in v1.

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Search Behavior

- Keep unified search in scope for v1.
- Discover search is grouped text search, not place search.
- A query should be matched independently against `People` and `Adventures`, then rendered as two sections in a single vertically scrolling result screen.
- `People` appears first.
- `Adventures` appears below it.
- If one section has no results, omit that section and keep the other section in the same single scroll.
- Do not use segmented tabs, nested scrolling areas, or separate result pages for `People` and `Adventures`.

- `People` search behavior:
  - use existing searchable profile fields already supported by the profile discovery foundation
  - base v1 matching on display name and handle
  - order people results using the same simple adventurer ranking used by `Explore Adventurers` when tie-breaking is needed

- `Adventures` search behavior:
  - search currently stored adventure fields that are safe and straightforward to support in v1
  - title is the required match field
  - description and place label may be included only if the live contract already exposes them cleanly and implementation remains straightforward
  - order adventure results by text relevance first, then publish recency as a tie-breaker

- explicit `Dakota` example:
  - if a user types `Dakota`, Discover should return:
    - `People`: adventurers whose display name or handle matches `Dakota`
    - `Adventures`: adventures whose searchable text fields match `Dakota`
  - Discover should not interpret `Dakota` as a geographic request for all adventures in North Dakota or South Dakota
  - geographic intent remains owned by the completed map/location-search experience

## Public Interface Expectations

- `GET /api/discover/home`
- `GET /api/discover/search`
- grouped Discover response types for adventurers and adventures
- no new `sort=best` requirement on `GET /api/profiles/:handle` for this feature

## Ranking And Data Strategy

- Ranking stays server-owned, but v1 ordering should be deliberately simple.
- Use only data already stored or already projected safely:
  - public published adventure count
  - published timestamps
  - category mix
  - favorite count
  - comment count
  - rating count and average rating where already derived
  - author display and location fields when present
- Use simple text matching for search; do not require geocoding, destination inference, or place expansion.
- Do not require:
  - recommendation reasons
  - destination metadata
  - Discover-specific telemetry
  - personalization
  - editorial curation flags
  - category home modules

## Saved And Favorites Placement

- Replacing the reserved `Saved` tab with `Discover` is a navigation and product-positioning decision, not a statement that saved content is unimportant.
- Saved and favorited browsing should move under later profile collections and favorites work rather than remain a main-tab destination.
- `Profile Collections` remains the follow-on feature that should absorb saved and authored-content browsing surfaces.
- `Favorites` remains the separate follow-on feature that should own save and unsave mechanics plus favorite-state hydration.

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [ ] server tests added for discover home and discover search
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Implementation Defaults

- Tab name is `Discover`.
- Discover becomes the next feature to implement after completed `Sidekicks + Profile Discovery` work.
- `Profile Collections` remains a separate later feature focused on profile-surface collections.
- `Favorites` remains a separate later feature focused on save and unsave mechanics plus favorite-state hydration.
- v1 is intentionally simpler than the prior draft because it must match current data reality.
- If profile or adventure fields are sparse, the UI should fall back gracefully rather than inventing content.

## Non-Goals

- Do not turn Discover into a DM, inbox, or chat surface.
- Do not optimize the screen around friendship mechanics, interest groups, or community management.
- Do not make Discover a clone of the local feed or the map experience.
- Do not introduce a second profile concept that competes with the existing profile flow.
- Do not add browse-by-category, destination, or rising-explorer home modules in v1.
- Do not add recommendation-reason copy or destination-oriented search behavior.
- Do not expand ambiguous text queries like `Dakota` into map-region results.

## Notes

- Discover is about place discovery without becoming a second place-search system.
- Adventurers are present because people help users browse public adventures, not because the app is becoming a social-network product.
- Saved and favorited items are no longer a main-tab destination and should land under later profile-based collection surfaces.
