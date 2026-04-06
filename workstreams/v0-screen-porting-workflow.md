# Workstream Support: v0-to-SwiftUI Screen Porting Workflow

Use this workflow for every remaining screen that moves from `v0-hidden-adventures-ui` into `hidden-adventures-ios`.

## Purpose

Make screen ports repeatable across repos by locking one common process for:

- where to find the v0 source artifacts
- how to resolve conflicts between React, screenshots, and specs
- how to sequence mock-first SwiftUI implementation and later live-data hookup
- what documentation and testing each screen port must leave behind

## Owning Repos

- visual source: `v0-hidden-adventures-ui`
- planning and workflow source: `hidden-adventures-plan`
- native implementation source: `hidden-adventures-ios`

## Required Artifact Set

Every screen port must gather all four artifact classes before implementation starts.

### 1. Primary React screen

- `../v0-hidden-adventures-ui/components/screens/<screen-name>.tsx`

Use this for:

- section ordering
- view hierarchy
- local UI state
- conditional rendering
- interaction expectations

### 2. Supporting React components

- `../v0-hidden-adventures-ui/components/**/*.tsx`

Read any supporting components that affect behavior or density, especially:

- image carousels
- bottom bars
- composers
- cards
- modals or sheets
- reusable rows that shape layout rhythm

### 3. Screenshot references

- `../v0-hidden-adventures-ui/docs/screenhots/<ScreenName>*.png`

Use screenshots as the final visual truth for:

- spacing
- overlap and scroll behavior
- corner radius and chip density
- vertical rhythm
- comment and card shapes
- visual hierarchy when React and Tailwind leave room for interpretation

Note: the folder name is intentionally `screenhots` and automation should use that exact path until the source repo changes it.

### 4. UX or design spec

- `../v0-hidden-adventures-ui/docs/ux-specs/<ScreenName>Design.md`

Use the spec for:

- section semantics
- copy intent
- native handoff expectations such as Maps or Share
- screen-level data requirements

If a screen-specific spec is missing, use the nearest approved UX note and record that gap in the screen handoff.

## Artifact Precedence

When artifacts disagree, resolve in this order:

1. screenshots for visual decisions
2. UX spec for intent and semantics
3. React code for structure, state, and conditional behavior

If native iOS should diverge for ergonomics, accessibility, or platform safety, record that divergence explicitly in the relevant plan note or screen handoff. Do not let it happen silently.

## Standard Porting Sequence

### Phase 1: Mock-data parity

1. Identify and read the full v0 artifact set.
2. Extract the screen sections, local state, and interaction rules from React.
3. Lock spacing, overlap, and density from screenshots.
4. Lock semantics and native behavior expectations from the UX spec.
5. Introduce a native screen model such as `<ScreenName>ScreenModel`.
6. Build the first SwiftUI screen against fixtures only.
7. Add deterministic variants for the main visual states.
8. Preserve or add a gallery/debug route for direct rendering.
9. Add stable accessibility identifiers for critical UI.
10. Compare native screenshots against the v0 screenshots before signoff.

### Phase 2: Live-data hookup

1. Keep the SwiftUI surface driven by the screen model.
2. Add a mapper from the live payload into that model.
3. Define explicit loading, success, empty, and error states.
4. Keep fixture mode intact after integration.
5. Rerun gallery screenshots after hookup to catch visual regressions.

## Native Implementation Rules

- do not bind SwiftUI views directly to server DTOs when the screen can be modeled more clearly with a screen model
- preserve fixture-backed previews for the main variants, including long text and empty states where relevant
- preserve the `UITEST_START_SCREEN` or gallery launch path for screens that already participate in the UI harness
- treat stable `accessibilityIdentifier` coverage as part of the implementation, not optional cleanup

## Minimum Identifier Coverage

Each screen port should expose identifiers for:

- primary navigation controls
- hero media or carousel
- title and location labels
- section headers used in UI regression tests
- primary CTA or sticky bottom controls
- interactive controls such as favorite, share, follow, rating, filters, or send actions
- repeated content areas likely to be targeted in UI tests

## Acceptance Checklist

A screen port is not done until:

1. fixture mode renders correctly
2. deterministic previews exist for the important variants
3. the gallery or direct-launch route still works
4. critical identifiers are present
5. generated screenshots have been compared against the matching v0 references
6. any native divergence has been written down explicitly
7. the live-data hookup, if complete, does not remove fixture coverage

## Screen Handoff Template

Each completed screen should record:

- primary v0 screen file used
- supporting component files used
- screenshot files used
- UX spec file used
- native screen model introduced
- fixture variants added
- identifiers added
- native deviations from v0, if any
- visual signoff status
- live-data hookup status
