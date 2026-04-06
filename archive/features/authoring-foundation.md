# Feature Family: Authoring Foundation

## Scope

- create adventure flow
- edit adventure flow
- uploads and media ownership path
- category and location entry
- visibility controls in the rebuilt model

## Program Role

- This document no longer represents a future implementation slice.
- It is the feature-family definition for the first post-Slice-1 scheduled work.
- Status and sequencing still flow through `hidden-adventures-plan`.

## Ordered Features In This Family

1. Create Adventure
2. Edit Adventure

## Delivery Loop

Each feature in this family should move through the standard post-Slice-1 execution loop:

1. design in `v0-hidden-adventures-ui`
2. mock or fixture-backed SwiftUI implementation in `hidden-adventures-ios`
3. required API additions in `hidden-adventures-server`
4. real iOS integration against the implemented APIs

Automation and manual QA are required at each applicable step before the feature is treated as complete.

## Acceptance Criteria

- [ ] create and edit UX is defined with an explicit screen map
- [ ] visibility controls align with the rebuild visibility model
- [ ] upload and media lifecycle expectations are documented
- [ ] server contract additions are defined without reworking completed feature contracts implicitly
- [ ] native behavior notes are documented for any deliberate divergence from the visual reference
- [ ] create adventure passes the full delivery loop and feature completion gates
- [ ] edit adventure passes the full delivery loop and feature completion gates

## Feature Completion Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [ ] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Readiness Gates

- [x] Slice 1 contract lock complete
- [x] Slice 1 milestone closed in the planning repo
- [x] deployment baseline exists for later operational validation

## Local Test Checklist

- [ ] use approved authoring UX references only
- [ ] validate proposed contract additions against the existing visibility and media model
- [ ] keep fixture-backed gallery coverage intact during native implementation
- [ ] document acceptance criteria before implementation starts

## Staging Validation Checklist

- [ ] not required for feature completion
- [ ] defer staging validation to the later operational phase unless a specific authoring dependency requires it earlier

## Migration Impact

- none expected

## Rollback Notes

- keep authoring sequencing deliberate until the active feature is intentionally started
