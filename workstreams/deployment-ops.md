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

- [x] image versioning convention
- [x] deploy checklist
- [x] rollback checklist
- [x] secrets and environment doc
- [x] staging validation checklist
- [ ] first real staging smoke execution record

## Dependencies

- backend runtime foundation
- Slice 1 contract stability for the first smoke flow

## Current State

- local Docker development is bootstrapped and usable
- a first deployment baseline now exists under `hidden-adventures-server/deploy/`
- image versioning, rollout and rollback steps, env templates, and a staging smoke script are documented and checked in
- the approved environment model now assumes local is the primary non-production validation surface, with no required dedicated staging environment in this phase
- production assumptions are now tied to the cross-repo testing and environment baseline in `workstreams/testing-environments.md`
- this remains a separate enabling lane and should not block Slice 2 definition work
- the remaining work is execution: the team still needs to run the first real staging smoke path without ad hoc server edits

## Done Means

- a tested image can be promoted to cloud
- production deploy does not require manual code edits on server
- rollback steps are documented and dry-run ready
