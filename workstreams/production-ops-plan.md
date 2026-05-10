# Workstream: Production API Operations Implementation Plan

This document is the canonical production API operations plan for the rebuild program. It supersedes [deployment-ops.md](./deployment-ops.md) for API runtime topology, deployment flow, operating procedures, and rollout sequencing.

## Goal

Stand up a lean, repeatable production API service for Hidden Adventures iOS clients on the existing Lightsail VM using:

- Caddy for host-level HTTPS and public API routing
- Docker Compose for the API and PostgreSQL runtime
- Amazon ECR for immutable image promotion
- a push-button solo deploy flow for the API
- optional GitHub Actions automation later, if it clearly reduces operator effort
- S3-backed PostgreSQL backups
- source-controlled SOPs in the scripts repo for routine operation, rollback, diagnostics, and restore

## Why This Plan Changed

The earlier deployment outline assumed a Lightsail load balancer in front of the VM. This newer plan moves TLS termination and routing onto the VM with Caddy. That decision changes the implementation order and the operational surface:

- it removes the extra load balancer layer, which lowers cost and configuration overhead
- it keeps public routing and TLS in one explicit host-level config
- it still preserves immutable deployments, digest-aware promotion discipline, and rollback readiness
- it accepts a simpler first production baseline in exchange for fewer moving pieces

This means the new work is not just "deploy Compose" but "build a complete API operating contract" covering DNS, HTTPS, reverse proxying, container lifecycle, release automation, backups, and operator procedures.

## Fixed Decisions And Rationale

### Runtime shape

- Use one existing Lightsail VM as the production host.
- Run `caddy` directly on the host.
- Run `api` and `postgres` in Docker Compose for this plan.
- Keep `admin` out of the active production baseline until a separate admin plan exists.
- Store legal/static pages at `/var/www/hidden-adventures/public`.

Why:

- It matches the current desire to avoid Terraform, Kubernetes, and broader infra automation.
- It keeps production close to local Docker development.
- It gives explicit control over public API routing without introducing another AWS resource layer first.

### Public domains for this plan

- `hiddenadventures.lucidios.com` serves the public entrypoint.
- `admin-adventures.lucidios.com` is reserved for future admin work and is not required for the production API baseline.

Why:

- The public API endpoint is the only domain required to complete this plan.
- Reserving the admin domain avoids re-deciding naming later without letting admin work delay the API baseline.

### Deployment model

- Build and test the API locally first.
- Push immutable API images to ECR from the laptop with the scripts-repo release command.
- Deploy by explicit image reference from the VM.
- Keep deploy tracking lightweight and automatic enough for one-person rollback safety.

Why:

- Digest-based promotion keeps production reproducible.
- Avoiding server-side compilation keeps production simpler and more repeatable.
- A script-first workflow fits the current one-person operating model better than a heavy release pipeline.
- Rollback stays simple when the previous known-good image is clearly recorded.

### Database placement

- Run PostgreSQL in Compose on the same VM for v1.

Why:

- It minimizes moving parts for the first production baseline.
- It is consistent with the current goal of speed and simplicity over early managed-infra complexity.
- It requires stronger backup and restore discipline because app and database live on the same host.

## Target Runtime Architecture

```text
Internet
  |
  +-- hiddenadventures.lucidios.com
  |     |
  |     +-- Caddy on host
  |           +-- /api -> api container :3000
  |           +-- /public -> /var/www/hidden-adventures/public
  |           +-- / -> static file server
  |
  +-- admin-adventures.lucidios.com
        |
        +-- reserved for future admin plan

Docker Compose
  +-- api
  +-- postgres

Host paths
  +-- /opt/hidden-adventures
  +-- /var/www/hidden-adventures/public
```

## Implementation Phases

### Phase 1: Confirm production inputs before touching the VM

#### Step 1. Verify the fixed public inputs

- Confirm the Lightsail static IP already exists and is attached to the target VM.
- Confirm the public API DNS record points at that static IP.
- Confirm the production API domain is final:
  - `hiddenadventures.lucidios.com`

Why:

- TLS issuance and public smoke checks will fail if DNS is not settled first.
- Avoiding host changes before the public routing inputs are stable reduces false debugging.

#### Step 2. Decide the minimum AWS assets needed for v1

- Create or confirm one ECR repository for the API image.
- Create or confirm one S3 bucket for production database backups.
- Create or confirm IAM credentials for the VM with access limited to:
  - ECR pull
  - S3 backup upload

Why:

- The runtime host should only be able to pull deploy artifacts and upload backups.
- Keeping permissions narrow lowers blast radius if the host is compromised.

#### Step 3. Inventory production secrets and environment variables

- Define the final contents for:
  - `/opt/hidden-adventures/env/api.env`
  - `/opt/hidden-adventures/env/postgres.env`
  - `/opt/hidden-adventures/env/deploy.env`
- Separate variables into:
  - application runtime config
  - database credentials
  - deployment metadata such as `API_IMAGE`

Why:

- Secret sprawl becomes much harder to clean up after the host is already live.
- Explicit env ownership keeps deploy scripts and Compose files simpler and safer.

### Phase 2: Prepare the host runtime

#### Step 4. Install and enable the core host packages

Run on the Lightsail VM:

```bash
sudo apt update
sudo apt install -y docker.io
sudo apt install -y docker-compose-plugin
sudo apt install -y caddy
sudo apt install -y awscli
sudo usermod -aG docker ubuntu
```

Then re-login as `ubuntu`.

Why:

- This is the minimum host surface needed to terminate HTTPS, run containers, and pull from AWS.
- Avoiding extra host services keeps the VM operational model narrow and easier to debug.

#### Step 5. Create the host directory layout

Run:

```bash
sudo mkdir -p /opt/hidden-adventures/{env,scripts,backups,staged}
sudo mkdir -p /var/www/hidden-adventures/public
sudo chown -R ubuntu:ubuntu /opt/hidden-adventures
```

Why:

- Runtime files, operator scripts, and backups need clear ownership boundaries.
- Keeping static public content outside the container runtime makes legal-page serving more durable and easier to inspect.

#### Step 6. Clone the production ops bundle repo and apply the managed host assets

On the Lightsail VM:

```bash
cd /opt
git clone <public-hidden-adventures-scripts-repo-url> hidden-adventures-scripts
cd /opt/hidden-adventures-scripts
sh scripts/apply.sh
```

This repo is now the canonical source for:

- `/opt/hidden-adventures/docker-compose.yml`
- `/opt/hidden-adventures/scripts/*.sh`
- `/opt/hidden-adventures/staged/Caddyfile`
- `/var/www/hidden-adventures/public/*`

Real env files remain local to the server under `/opt/hidden-adventures/env` and are not committed to the public repo.

Why:

- The VM should consume source-controlled host assets rather than hand-authored files copied from markdown snippets.
- The public smoke checks already depend on the legal pages that the apply step installs.

### Phase 3: Configure host-level HTTPS and routing

#### Step 7. Install the staged production Caddyfile

The ops bundle repo stages the canonical config at:

```bash
/opt/hidden-adventures/staged/Caddyfile
```

Install it explicitly with:

```bash
sudo cp /opt/hidden-adventures/staged/Caddyfile /etc/caddy/Caddyfile
```

Why:

- Caddy gives automatic HTTPS with a smaller config footprint than managing Nginx plus certbot.
- Binding the app containers to loopback-only ports keeps them off the public interface.
- Keeping routing at the host level makes container networking easier to inspect and operate.

#### Step 8. Validate and reload Caddy

Run:

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
sudo systemctl status caddy
```

Why:

- Caddy config issues are easier to fix before the application containers are in the mix.
- Separating config validation from app rollout narrows the source of any HTTPS failure.

### Phase 4: Define the container runtime

#### Step 9. Apply the production Compose file and keep local env files on the VM

The ops bundle repo owns the canonical `docker-compose.yml` and installs it into:

```bash
/opt/hidden-adventures/docker-compose.yml
```

The repo also carries example env templates for reference, but the real runtime env files stay server-local.

Why:

- Loopback-only published ports let Caddy stay the single public ingress.
- `restart: unless-stopped` is sufficient for a single-host baseline without introducing orchestration complexity.
- A named Docker volume is the minimum acceptable persistence layer for v1 Postgres on-host.

#### Step 10. Create the production env files

Create:

- `/opt/hidden-adventures/env/api.env`
- `/opt/hidden-adventures/env/postgres.env`
- `/opt/hidden-adventures/env/deploy.env`

Seed `postgres.env` with:

```dotenv
POSTGRES_DB=hidden_adventures
POSTGRES_USER=hidden_adventures
POSTGRES_PASSWORD=<strong-password>
```

Seed `deploy.env` with:

```dotenv
API_IMAGE=<initial-api-image-ref>
```

Why:

- Splitting env files by service keeps credential boundaries clear.
- The Compose file becomes stable while secrets rotate independently.

#### Step 11. Start the runtime locally on the VM once before API release automation

Run:

```bash
cd /opt/hidden-adventures
docker compose config
docker compose up -d
docker compose ps
```

Why:

- The first successful boot should happen with the smallest possible moving surface.
- It is easier to debug Compose, env files, and host networking before release automation is involved.

### Phase 5: Build API release automation in the scripts repo

Goal: create the push-button release interface used by every later phase.

Repo: `hidden-adventures-scripts`

Artifacts to create or modify:

- `scripts/release-api.sh`
- `SOPs/api-release.md`
- `SOPs/api-rollback.md`

Required `release-api.sh` commands:

- `push`: build the API image from the server repo, tag it with git SHA plus timestamp, push it to ECR, resolve the digest, and print the immutable image ref.
- `deploy <image-ref>`: update the production API image ref, invoke the server-side deploy flow, run migrations, restart `api`, run smoke checks, and log the result.
- `ship`: run `push`, then deploy the exact image that was just pushed.
- `rollback <image-ref>`: deploy a previous image ref, run smoke checks, and log the rollback.

Required config contract:

- The script reads local operator config from a scripts-repo env file such as `.env.production.local`; this file is never committed.
- The production VM stores runtime config under `/opt/hidden-adventures/env`.
- The deployed API image is recorded in `/opt/hidden-adventures/env/deploy.env` as `API_IMAGE=<immutable-image-ref>`.
- Deploy history is appended on the VM to `/opt/hidden-adventures/deploy-log.jsonl`.

Acceptance checks:

- `scripts/release-api.sh --help` documents every command and required env var.
- `scripts/release-api.sh push --dry-run` validates local config without pushing.
- `scripts/release-api.sh deploy --dry-run <image-ref>` shows the SSH and deploy steps without changing production.
- `SOPs/api-release.md` and `SOPs/api-rollback.md` explain the exact operator commands for normal release and rollback.

Handoff to Phase 6:

- Codex can open `hidden-adventures-scripts` and implement `scripts/release-api.sh` plus the first two API SOPs before touching server runtime behavior.

### Phase 6: Make the production runtime API-only

Goal: ensure the VM Compose runtime runs `postgres` and `api`, with `admin` absent or disabled.

Repo: `hidden-adventures-scripts`

Artifacts to create or modify:

- production `docker-compose.yml`
- env templates or examples for `api.env`, `postgres.env`, and `deploy.env`
- `scripts/apply.sh`
- `scripts/deploy.sh`

Required behavior:

- `api` uses `API_IMAGE` from `/opt/hidden-adventures/env/deploy.env`.
- `postgres` remains the only database service.
- `admin` is not part of the active production baseline.
- `deploy.sh` pulls `API_IMAGE`, runs migrations with the API image, starts or restarts `api`, and leaves `postgres` running.
- `apply.sh` installs or updates the scripts, Compose file, public assets, Caddy staging file, and `SOPs/` folder onto the server.

Acceptance checks:

- `docker compose config` succeeds on the VM.
- `docker compose ps` shows `postgres` and `api` after deploy.
- `admin` is not required for the production API baseline.
- A reboot recovery check confirms Compose can bring the API runtime back up cleanly.

Handoff to Phase 7:

- The VM is ready to receive a real API image from ECR and run it without admin services.

### Phase 7: Prove API deploy end to end

Goal: ship the first real API image from local development to production.

Repos:

- `hidden-adventures-server`
- `hidden-adventures-scripts`

Required flow:

1. Run the server repo's local test and build validation.
2. Run `scripts/release-api.sh push` from the scripts repo.
3. Capture the immutable image ref printed by the script.
4. Run `scripts/release-api.sh deploy <image-ref>` or `scripts/release-api.sh ship`.
5. Confirm the deploy log entry includes timestamp, git SHA, release tag, image ref, previous image ref, migration result, and smoke result.

Acceptance checks:

- VM pulls the image from ECR.
- Migrations complete successfully.
- `api` starts successfully.
- Caddy routes public API traffic to the container.
- Smoke checks pass against `hiddenadventures.lucidios.com`.
- The previous image ref is available for rollback.

Handoff to Phase 8:

- The production API is deployed and reachable through the public domain, so the iOS client can be pointed at it.

### Phase 8: Connect the iOS client to the production API

Goal: prove the production API can serve an iOS development build.

Repo: `hidden-adventures-ios`

Required behavior:

- Add or verify a production API base URL configuration for development builds.
- Ensure the client can target `https://hiddenadventures.lucidios.com`.
- Run the current client flow against production for the API paths already implemented.
- Keep this as a development-build verification milestone, not TestFlight or App Store readiness.

Acceptance checks:

- iOS dev build reaches the production API through HTTPS.
- Core read paths work from the app.
- Auth works if required by the currently implemented client flow.
- No localhost or LAN-only assumptions remain in the selected production API configuration path.

Handoff to Phase 9:

- The API is serving a real client path, so database backup and restore can be hardened before routine operation.

### Phase 9: Add backups and restore SOPs

Goal: make on-host Postgres acceptable for routine API operation.

Repo: `hidden-adventures-scripts`

Artifacts to create or modify:

- `scripts/backup-postgres.sh`
- `scripts/restore-postgres.sh` or a documented restore command sequence if a script is too risky
- `SOPs/db-backup.md`
- `SOPs/db-restore.md`

Required behavior:

- Backups run with `pg_dump -Fc`.
- Backups upload to the configured S3 bucket.
- Backup output includes enough metadata to identify database, timestamp, and source host.
- Restore SOP covers restore into a fresh volume or replacement container without overwriting production by accident.
- Cron is installed for daily backup after manual backup succeeds.

Acceptance checks:

- Manual backup uploads to S3 successfully.
- Scheduled backup is installed.
- Restore rehearsal succeeds against a non-production target or disposable restore volume.
- SOP identifies the latest restore point and the command sequence to use during an incident.

Handoff to Phase 10:

- Backup and restore are real operating capabilities, so the remaining work is to gather all operator procedures into a usable runbook set.

### Phase 10: Write operator SOPs and production readiness checklist

Goal: make production operation possible without rediscovering commands during stress.

Repo: `hidden-adventures-scripts`

Required SOP folder contents:

- `SOPs/api-release.md`
- `SOPs/api-rollback.md`
- `SOPs/api-smoke-checks.md`
- `SOPs/api-diagnostics.md`
- `SOPs/db-backup.md`
- `SOPs/db-restore.md`
- `SOPs/server-reboot-recovery.md`

Required SOP content:

- Each SOP starts with `When to use this`.
- Each SOP lists exact commands.
- Each SOP names expected success signals.
- Each SOP names stop conditions where the operator should not keep improvising.
- SOPs must be copied to the Lightsail server by `apply.sh`.

Acceptance checks:

- SOPs are present in the scripts repo.
- SOPs are present on the server after `apply.sh`.
- A fresh Codex agent can follow the SOPs without needing context from this chat.
- The production readiness checklist below passes.

## Production Readiness Criteria

The production API baseline is complete only when all of these are true:

- API images can be built locally and pushed to ECR with `scripts/release-api.sh push`.
- A pushed image can be deployed with `scripts/release-api.sh deploy <image-ref>`.
- `scripts/release-api.sh ship` can push and immediately deploy one image.
- `scripts/release-api.sh rollback <previous-image-ref>` can restore the previous API image.
- The VM runs `postgres` and `api` without requiring `admin`.
- API deploy runs migrations and smoke checks automatically.
- Deploy log records current and previous image refs.
- iOS dev build can talk to the production API domain.
- Daily Postgres backup uploads to S3.
- Restore has been rehearsed once.
- SOPs exist in the scripts repo and are installed onto the Lightsail server.

## Future Work Not Covered By This Plan

Do not include these as numbered phases in the production API plan:

- Admin console implementation.
- Admin container production deployment.
- Admin ECR repository and admin release automation.
- GitHub Actions as the primary release system.
- TestFlight or App Store production client rollout.
- Managed Postgres migration.
- Load balancer, Terraform, Kubernetes, or broader observability stack.

Create separate formal plans for these later, after the production API service is operating reliably.

## Non-Goals

- Terraform
- Kubernetes
- managed Postgres for v1
- a separate load balancer tier
- Grafana or a broader observability platform for the first rollout
- a standing pre-production environment
- making GitHub Actions mandatory for production release
- shipping the admin console in the first production API milestone

## Recommended Execution Order

1. Confirm DNS, domains, ECR, S3, and IAM inputs.
2. Prepare the VM packages and directory layout.
3. Clone the public ops bundle repo and create local env files.
4. Apply the repo-managed runtime, public, and staged Caddy assets.
5. Install and validate Caddy.
6. Boot the runtime manually on the VM once with the current Postgres-only state.
7. Build `scripts/release-api.sh` and the API release/rollback SOPs in `hidden-adventures-scripts`.
8. Make the production Compose and deploy scripts API-only.
9. Run the first API image push and production deploy using an immutable image ref.
10. Connect an iOS dev build to the production API domain.
11. Add backup automation, restore support, and DB SOPs.
12. Complete the full SOP folder and production readiness checklist.

## Done Means

- Hidden Adventures has an operating production API service on the existing Lightsail VM.
- HTTPS and public API routing are handled by a stable host-level Caddy config.
- The VM runs `postgres` and `api` without requiring `admin`.
- The public API and legal pages pass repeatable smoke checks after deploy.
- The API release flow is push-button for one operator: push, deploy, ship, and rollback all use the same script family.
- The iOS dev build can talk to the production API domain.
- The database is backed up to S3 automatically and restore steps have been rehearsed.
- SOPs exist in the scripts repo, are installed onto the server, and cover release, rollback, smoke checks, diagnostics, DB backup, DB restore, and reboot recovery.
