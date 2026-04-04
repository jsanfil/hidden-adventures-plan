# Workstream: Product and UX

## Goal

Redesign Hidden Adventures around modern journeys, strong visual identity, and a cleaner social model, while keeping Slice 1 stable enough for contract lock and real client integration.

## Scope

- information architecture
- navigation model
- feed, map, detail, create, and edit flows
- mutual-connections concept
- visibility and sharing UX
- design system direction

## Deliverables

- [ ] jobs-to-be-done summary
- [ ] durable screen map beyond the current Slice 1 route map
- [ ] Slice 2 create and edit flow specification
- [x] visibility model recommendation
- [x] Slice 1 visual reference in `v0-hidden-adventures-ui`
- [x] Slice 1 route map established for native implementation

## Dependencies

- legacy audit
- PRD review
- Slice 1 scope stability

## Current State

- Slice 1 visual exploration exists and has already informed the native SwiftUI shell.
- The current product and UX priority is no longer basic Slice 1 invention; it is protecting Slice 1 stability while moving Slice 2 definition forward in parallel.
- The next UX output should be a durable screen map and implementation-ready Slice 2 flow set rather than more open-ended Slice 1 exploration.

## Direction Notes

- Use the legacy PRD as feature-floor input, not as the rebuild UI blueprint.
- Preserve the core product loops: discover, inspect, create, save, discuss, connect, and get help.
- Rework the sidekicks and visibility concepts into a cleaner modern social and sharing model.
- Favor a coherent exploration system over a literal recreation of the old tab or storyboard structure.
- Do not change Slice 1 contracts or navigation implicitly while working on Slice 2 design.

## Source of Truth

- `hidden-adventures-plan` owns product intent, release scope, slice boundaries, information architecture, and acceptance criteria.
- `v0-hidden-adventures-ui` owns Slice 1 visual exploration and is the primary reference for composition, spacing, typography, icon rhythm, and surface styling.
- `hidden-adventures-ios` owns the native SwiftUI implementation and any explicit native behavior decisions.

## Slice 1 Route Map

- `welcome -> email auth -> bootstrap -> (profile setup for new users only) -> explore shell (feed/map) -> adventure detail`
- Treat feed and map as two modes of one exploration system, even if the v0 reference presents them as separate screens.
- `Get Started` and `Sign In` are not duplicate buttons: they express user intent and affect post-auth framing, while backend bootstrap remains authoritative about whether the user is linked or new.

## Slice 2 Output Expectations

- define create and edit journey states clearly enough for backend and iOS threads to consume without re-deciding product intent
- document visibility UX copy and control states against the rebuild visibility model
- expand the screen map beyond the current Slice 1 shell so later slices do not rely on scattered v0 references alone

## v0-to-SwiftUI Workflow

- Design and refine approved visuals in `v0-hidden-adventures-ui`.
- If a v0 change affects navigation, scope, or interaction model beyond visual fidelity, update this plan repo before native implementation.
- Port approved screens natively into `hidden-adventures-ios`.
- Add or update stable accessibility identifiers for any visually critical UI touched by the change.
- Validate native parity with `hidden-adventures-ios/Scripts/run_ui_gallery.sh`.
- Compare generated iOS screenshots against the v0 screen or approved screenshot reference before closing a parity task.

## Native Behavior Override

- v0 is the visual reference, not a requirement to copy web behavior literally.
- SwiftUI may intentionally diverge for better native ergonomics, accessibility, or layout safety, but that divergence must be recorded explicitly in the workstream or plan instead of being made silently.

## Reference

- [migration/prd-modernization-baseline.md](../migration/prd-modernization-baseline.md)
- [workstreams/visibility-model.md](./visibility-model.md)

## Done Means

- Slice 1 remains stable for integration work
- Slice 2 flow definitions are implementation-ready
- social and visibility concepts are explicit enough that backend and client work do not need to infer product intent
