# Slice 2: Create And Share

## Scope

- create adventure flow
- edit adventure flow
- uploads and media ownership path
- category and location entry
- visibility controls in the rebuilt model

## Current Status

- definition and UX incubation only
- no Slice 2 implementation should start until Slice 1 is documented, integrated, and locally testable end to end

## Acceptance Criteria

- [ ] create and edit UX is defined with an explicit screen map
- [ ] visibility controls align with the rebuild visibility model
- [ ] upload and media lifecycle expectations are documented
- [ ] server contract additions are defined without reworking Slice 1 contracts implicitly
- [ ] native behavior notes are documented for any deliberate divergence from the visual reference

## Readiness Gates

- [ ] Slice 1 contract lock complete
- [ ] Slice 1 local end-to-end acceptance complete
- [ ] deployment baseline exists for future slice smoke tests

## Local Test Checklist

- [ ] use approved Slice 2 UX references only
- [ ] validate proposed contract additions against the existing visibility and media model
- [ ] document acceptance criteria before implementation starts

## Staging Validation Checklist

- [ ] not applicable until Slice 2 implementation begins

## Migration Impact

- none expected

## Rollback Notes

- keep Slice 2 as a definition-only track until Slice 1 closes
