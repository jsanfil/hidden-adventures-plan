# Workstream: Product and UX

## Goal

Redesign Hidden Adventures around modern journeys, strong visual identity, and a cleaner social model before schema and API freeze.

## Scope

- information architecture
- navigation model
- feed, map, detail, and creation flows
- mutual-connections concept
- visibility and sharing UX
- design system direction

## Deliverables

- [ ] jobs-to-be-done summary
- [ ] navigation and screen map
- [ ] social graph recommendation
- [x] visibility model recommendation
- [ ] design system moodboard and UI principles (in progress)
- [x] clickable prototype for slice 1 in `v0-hidden-adventures-ui`

## Dependencies

- legacy audit
- PRD review

## Direction Notes

- Use the legacy PRD as feature-floor input, not as the rebuild UI blueprint.
- Preserve the core product loops: discover, inspect, create, save, discuss, connect, and get help.
- Rework the sidekicks and visibility concepts into a cleaner modern social and sharing model.
- Favor a coherent exploration system over a literal recreation of the old tab/storyboard structure.

## Source of Truth

- `hidden-adventures-plan` owns product intent, release scope, slice boundaries, information architecture, and acceptance criteria.
- `v0-hidden-adventures-ui` owns slice-1 visual exploration and is the primary reference for composition, spacing, typography, icon rhythm, and surface styling.
- `hidden-adventures-ios` owns the native SwiftUI implementation and any explicit native behavior decisions.

## Slice 1 Route Map

- `welcome -> profile setup -> explore shell (feed/map) -> adventure detail`
- Treat feed and map as two modes of one exploration system, even if the v0 reference presents them as separate screens.

## v0-to-SwiftUI Workflow

- Design and refine slice-1 visuals in `v0-hidden-adventures-ui`.
- If a v0 change affects navigation, scope, or interaction model beyond visual fidelity, update this plan repo before native implementation.
- Port approved slice-1 screens natively into `hidden-adventures-ios`.
- Add or update stable accessibility identifiers for any visually critical UI touched by the change.
- Validate native parity with `hidden-adventures-ios/Scripts/run_ui_gallery.sh`.
- Compare generated iOS screenshots against the v0 screen or approved screenshot reference before closing a parity task.

## Native Behavior Override

- v0 is the visual reference, not a requirement to copy web behavior literally.
- SwiftUI may intentionally diverge for better native ergonomics, accessibility, or layout safety, but that divergence must be recorded explicitly in the workstream or plan instead of being made silently.

## Visual Review Inputs

- Use the live `v0-hidden-adventures-ui` components as the main visual reference.
- Use exported screenshots such as `/Users/josephsanfilippo/Downloads/vo-screenshots` when a static reference is useful.
- Use the native screenshot gallery from `hidden-adventures-ios` as the ongoing parity baseline for implemented screens.

## Reference

- [migration/prd-modernization-baseline.md](../migration/prd-modernization-baseline.md)
- [workstreams/visibility-model.md](./visibility-model.md)

## Done Means

- a prototype exists for slice 1
- social and visibility concepts are explicit
- backend schema can be locked without product ambiguity
