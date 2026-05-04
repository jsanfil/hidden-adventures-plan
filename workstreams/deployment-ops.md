# Workstream: Deployment and Ops

## Goal

Keep local development simple and production deployment cheap, repeatable, and safe.

## Summary

The initial production target is a lean VM plus load balancer shape:

- local desktop or CI builds one immutable server image
- the image is pushed to a private registry
- the pushed digest is recorded with the git SHA
- the production Lightsail VM pulls and runs that exact digest with Docker Compose
- a Lightsail load balancer sits in front for TLS termination and instance health checks
- PostgreSQL stays external to the app container
- Cognito and S3 stay as AWS-managed services outside Lightsail

This workstream is the canonical deployment and operations outline for the rebuild. It defines the production topology, promotion flow, rollback expectations, monitoring minimums, and the current decision to keep a dedicated pre-production host optional.

## Scope

- Docker image workflow
- registry strategy
- Lightsail runtime shape
- environment configuration
- release and rollback procedures
- monitoring and alerting expectations
- backup and restore expectations

## Deliverables

- [x] image versioning convention
- [x] deploy checklist
- [x] rollback checklist
- [x] secrets and environment doc
- [x] smoke-check script baseline
- [ ] first real optional smoke-environment execution record
- [ ] first production rehearsal record with digest capture and rollback notes

## Dependencies

- backend runtime foundation
- current server deploy assets in `hidden-adventures-server/deploy/`
- stable read-path smoke coverage for the currently shipped API surface

## Production Topology

### Runtime Shape

- `Lightsail load balancer`
  Public entrypoint, HTTPS termination, certificate attachment, and health checks.
- `Lightsail VM`
  Docker Compose host that runs the application container and nothing more than the minimum host services needed for Docker operation and operator access.
- `External PostgreSQL`
  Separate from the app container. Migrations run against this database before traffic is considered healthy on the new image.
- `AWS-managed dependencies`
  Cognito and S3 remain outside the VM and are configured through runtime environment variables.

### Why This Shape First

- It matches the current repo assumptions and deploy assets.
- It keeps the operational model close to local Docker development.
- It gives TLS termination and health checks without introducing a second web-server tier on the VM.
- It keeps the first production baseline cheap enough to operate while still leaving room to add redundancy later.

## Release Flow

The promoted runtime flow is:

1. Build an immutable image locally or in CI.
2. Push the image to a private registry.
3. Record the git SHA, image tag, and pushed image digest in a deploy log.
4. Run database migrations with that exact image.
5. Update the Lightsail VM runtime definition to the same image digest.
6. Restart the app container from that digest.
7. Verify the deployment through the public load balancer URL with smoke checks.
8. Keep the prior known-good digest ready for rollback.

### Promotion Rules

- Deploy by digest, not by mutable tag alone.
- Never rebuild or republish an existing release tag to point at a different commit.
- Treat production promotion as a host-runtime update, not a manual code edit on the VM.
- Keep a short deploy record for every rollout:
  - operator
  - environment
  - git SHA
  - pushed digest
  - migration result
  - smoke result
  - rollback target digest

## Registry Strategy

### Preferred Default

- Prefer private Amazon ECR when AWS access, auth, and operator workflow are already acceptable.

### Acceptable First Alternative

- Allow GHCR as a simpler early registry when ECR auth or IAM setup would otherwise slow down the first clean rollout.

### Decision Rule

- Use ECR if it is easy for the team to authenticate from both the build side and the Lightsail VM.
- Use GHCR if it materially reduces first-deploy friction, but keep digest-based promotion and the same rollout discipline.
- The registry choice should not change the runtime contract on the VM.

## TLS And Traffic Policy

- The Lightsail load balancer is the public HTTPS endpoint.
- The app container should continue serving plain HTTP on the VM's private listener.
- TLS termination, certificate attachment, and public health checks belong at the load balancer layer for this first baseline.
- Load balancer health checks should target a fast, purpose-built path such as `/api/health`.

### Why No Apache Or Nginx First

- A host-level web server is not required for basic HTTPS termination, simple API routing, or instance health checks in this topology.
- Deferring Apache or Nginx reduces host complexity, config drift, and another moving part during the first production rollout.
- Add an on-box web server later only if one of these becomes real:
  - host-level redirects or custom rewrite rules
  - advanced caching behavior
  - advanced rate limiting
  - WAF-adjacent controls not covered elsewhere
  - multiple co-hosted apps or mixed static and dynamic delivery needs

## Optional Smoke Environment

This program does not require a standing dedicated pre-production environment in the current phase.

Instead, the docs should use `optional smoke environment` for any temporary or semi-persistent pre-production host that exists only to validate the cloud deployment path. That environment is optional because:

- local validation remains the main non-production acceptance surface
- the server already has strong local Docker parity
- standing infrastructure cost should stay low until production rollout is routine

If a smoke environment exists, it should use the same topology as production on a smaller scale:

- one Lightsail VM
- one load balancer if public HTTPS validation matters
- the same image-promotion and smoke-check flow

## Rollback Baseline

- The default rollback is application-image rollback to the last known-good digest.
- Migrations should be treated as forward-only unless a specific down path has already been designed and tested.
- If a bad migration lands, prefer pausing promotion and applying a forward repair instead of improvising database rollback steps on the live environment.

Rollback checklist:

1. Identify the last known-good digest from the deploy log.
2. Point the VM runtime definition back to that digest.
3. Restart the app container.
4. Re-run smoke checks through the public entrypoint.
5. Capture the incident and any migration or runtime follow-up before the next deploy.

## Monitoring Minimums

### Application

- structured logs to stdout
- clear startup log that includes app version or git SHA when available
- deploy log that records digest, SHA, operator, migration result, and smoke result
- request and error logging sufficient to separate app failures from infrastructure failures

### Lightsail VM

- CPU utilization
- network saturation or unusual network spikes
- burst balance or similar host-capacity pressure if the selected plan exposes it
- disk usage and free space through host checks or equivalent operator review
- container restart loops and container health state

### Load Balancer

- unhealthy host count
- 5xx error count or rate
- response latency
- health-check pass or fail status

### Database

- CPU
- storage and free space
- connection pressure
- failed authentication or connection failures
- backup success state and latest restore point visibility

### Synthetic Checks

- post-deploy smoke against:
  - `GET /`
  - `GET /api/health`
  - `GET /api/feed`
  - `GET /api/adventures/:id` from feed output when available
  - `GET /api/profiles/:handle` from feed output when available

## Alerting Minimums

Classify alerts into three groups.

### Immediate Page

- load balancer unhealthy host count above `0`
- sustained 5xx errors above the established normal baseline
- production database critically low on free storage
- production database connection pressure high enough to threaten availability

### Same-Day Human Follow-Up

- sustained VM CPU saturation
- unusual network saturation or host-capacity pressure
- elevated latency without full outage
- repeated container restarts
- backup not observed on the expected daily cadence

### Deploy-Time Warning Only

- smoke failure on an optional smoke environment
- failed migration before traffic is considered healthy
- non-critical smoke degradation that does not affect current rollout scope but should block promotion until understood

For Lightsail-managed resources, alarms should be configured at minimum for the instance and load balancer metrics that map to the cases above. Non-Lightsail database alerting should use the database platform's own monitoring surface if the database does not live inside Lightsail.

## Backup And Restore Expectations

- production backups must be automated and observable
- backup success should be reviewed as part of production-readiness, not assumed
- restore steps must be written down before production is treated as routine
- app-image rollback and database restore are separate workflows and should not be conflated

## Current State

- local Docker development is bootstrapped and usable
- a first deployment baseline exists under `hidden-adventures-server/deploy/`
- image versioning, rollout and rollback steps, env templates, and smoke automation are already checked in
- the current environment model treats local validation as the primary non-production acceptance surface
- this workstream now defines the canonical topology and alerting baseline for the first production rollout
- a cross-repo follow-up remains open in `hidden-adventures-server/deploy/README.md` because its referenced filenames have drifted from the actual checked-in deploy files

## Done Means

- a tested image can be promoted to cloud by digest without ad hoc server edits
- the VM plus load balancer topology is documented clearly enough for a clean first rollout
- monitoring and alerting minimums are named with clear ownership
- rollback steps are documented and dry-run ready
- optional smoke-environment language is consistent with the rest of the planning repo
