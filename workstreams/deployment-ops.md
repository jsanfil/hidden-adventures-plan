# Workstream: Deployment and Ops

## Goal

Keep local development simple and production deployment cheap, repeatable, and safe.

## Scope

- Docker image workflow
- registry strategy
- Lightsail runtime shape
- environment configuration
- release and rollback procedures

## Deliverables

- [ ] image versioning convention
- [ ] deploy checklist
- [ ] rollback checklist
- [ ] secrets and environment doc
- [ ] staging validation checklist

## Dependencies

- backend runtime foundation
- Slice 1 contract stability for the first smoke flow

## Current State

- local Docker development is bootstrapped and usable
- production and staging guidance is still intentionally light
- this remains a separate enabling lane and should not block Slice 2 definition work
- this should close only after the team can perform a repeatable deploy, rollback, and smoke validation without ad hoc server edits

## Done Means

- a tested image can be promoted to cloud
- production deploy does not require manual code edits on server
- rollback steps are documented and dry-run ready
