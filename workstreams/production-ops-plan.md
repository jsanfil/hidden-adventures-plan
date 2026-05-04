# Workstream: Production Runtime & CI/CD Implementation Plan

This document is the canonical production-ops plan for the rebuild program. It supersedes [deployment-ops.md](./deployment-ops.md) for runtime topology, deployment flow, and rollout sequencing.

## Goal

Stand up a lean, repeatable production environment for Hidden Adventures on the existing Lightsail VM using:

- Caddy for host-level HTTPS, routing, and basic auth
- Docker Compose for the application runtime
- Amazon ECR for immutable image promotion
- GitHub Actions for CI/CD orchestration
- S3-backed PostgreSQL backups

## Why This Plan Changed

The earlier deployment outline assumed a Lightsail load balancer in front of the VM. This newer plan moves TLS termination and routing onto the VM with Caddy. That decision changes the implementation order and the operational surface:

- it removes the extra load balancer layer, which lowers cost and configuration overhead
- it keeps public routing, TLS, and basic auth in one explicit host-level config
- it still preserves immutable deployments, digest-aware promotion discipline, and rollback readiness
- it accepts a simpler first production baseline in exchange for fewer moving pieces

This means the new work is not just "deploy Compose" but "build a complete host runtime contract" covering DNS, HTTPS, reverse proxying, container lifecycle, backups, and operator procedures.

## Fixed Decisions And Rationale

### Runtime shape

- Use one existing Lightsail VM as the production host.
- Run `caddy` directly on the host.
- Run `api`, `admin`, and `postgres` in Docker Compose.
- Store legal/static pages at `/var/www/hidden-adventures/public`.

Why:

- It matches the current desire to avoid Terraform, Kubernetes, and broader infra automation.
- It keeps production close to local Docker development.
- It gives explicit control over routing and admin protection without introducing another AWS resource layer first.

### Public domains

- `hiddenadventures.lucidios.com` serves the public entrypoint.
- `admin-adventures.lucidios.com` serves the admin console.

Why:

- The separation keeps public and operator-facing traffic distinct.
- It allows the admin surface to use stricter controls without complicating the public app domain.

### Deployment model

- Build immutable images in CI.
- Push images to ECR.
- Deploy by explicit image reference from the VM.
- Record git SHA, image tag, and deployed digest for every rollout.

Why:

- Digest-based promotion keeps production reproducible.
- CI-driven builds avoid ad hoc server-side compilation.
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
        +-- Caddy on host
              +-- basic auth
              +-- -> admin container :3001

Docker Compose
  +-- api
  +-- admin
  +-- postgres

Host paths
  +-- /opt/hidden-adventures
  +-- /var/www/hidden-adventures/public
```

## Implementation Phases

### Phase 1: Confirm production inputs before touching the VM

#### Step 1. Verify the fixed public inputs

- Confirm the Lightsail static IP already exists and is attached to the target VM.
- Confirm both DNS records point at that static IP.
- Confirm the production domains are final:
  - `hiddenadventures.lucidios.com`
  - `admin-adventures.lucidios.com`

Why:

- TLS issuance and public smoke checks will fail if DNS is not settled first.
- Avoiding host changes before the public routing inputs are stable reduces false debugging.

#### Step 2. Decide the minimum AWS assets needed for v1

- Create or confirm one ECR repository for the API image.
- Create or confirm one ECR repository for the admin image.
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
  - `/opt/hidden-adventures/env/admin.env`
  - `/opt/hidden-adventures/env/postgres.env`
  - `/opt/hidden-adventures/.deploy.env`
- Separate variables into:
  - application runtime config
  - admin runtime config
  - database credentials
  - deployment metadata such as ECR registry URLs and image tags

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
sudo mkdir -p /opt/hidden-adventures/{env,scripts,backups}
sudo mkdir -p /var/www/hidden-adventures/public
sudo chown -R ubuntu:ubuntu /opt/hidden-adventures
```

Why:

- Runtime files, operator scripts, and backups need clear ownership boundaries.
- Keeping static public content outside the container runtime makes legal-page serving more durable and easier to inspect.

#### Step 6. Install the initial legal/public files

- Place the initial static assets under `/var/www/hidden-adventures/public`.
- Confirm at minimum:
  - `privacy-policy.html`
  - `terms-conditions.html`

Why:

- The public smoke checks already depend on these files.
- Serving them from the host avoids tying legal-page availability to container startup.

### Phase 3: Configure host-level HTTPS and routing

#### Step 7. Write the production Caddyfile

Create `/etc/caddy/Caddyfile`:

```caddy
hiddenadventures.lucidios.com {
    encode gzip

    root * /var/www/hidden-adventures

    handle /api/* {
        reverse_proxy 127.0.0.1:3000
    }

    handle /public/* {
        file_server
    }

    handle {
        file_server
    }
}

admin-adventures.lucidios.com {
    encode gzip

    basicauth {
        joe <HASH>
    }

    reverse_proxy 127.0.0.1:3001
}
```

Why:

- Caddy gives automatic HTTPS with a smaller config footprint than managing Nginx plus certbot.
- Binding the app containers to loopback-only ports keeps them off the public interface.
- Host-level basic auth is the fastest safe control for the v1 admin surface.

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

#### Step 9. Create the production Compose file

Create `/opt/hidden-adventures/docker-compose.yml`:

```yaml
services:
  api:
    image: ${API_IMAGE}
    restart: unless-stopped
    env_file:
      - ./env/api.env
    ports:
      - "127.0.0.1:3000:3000"
    depends_on:
      - postgres

  admin:
    image: ${ADMIN_IMAGE}
    restart: unless-stopped
    env_file:
      - ./env/admin.env
    ports:
      - "127.0.0.1:3001:3000"
    depends_on:
      - postgres

  postgres:
    image: postgis/postgis:16-3.4
    restart: unless-stopped
    env_file:
      - ./env/postgres.env
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Why:

- Loopback-only published ports let Caddy stay the single public ingress.
- `restart: unless-stopped` is sufficient for a single-host baseline without introducing orchestration complexity.
- A named Docker volume is the minimum acceptable persistence layer for v1 Postgres on-host.

#### Step 10. Create the production env files

Create:

- `/opt/hidden-adventures/env/api.env`
- `/opt/hidden-adventures/env/admin.env`
- `/opt/hidden-adventures/env/postgres.env`

Seed `postgres.env` with:

```dotenv
POSTGRES_DB=hidden_adventures
POSTGRES_USER=hidden_adventures
POSTGRES_PASSWORD=<strong-password>
```

Why:

- Splitting env files by service keeps credential boundaries clear.
- The Compose file becomes stable while secrets rotate independently.

#### Step 11. Start the runtime locally on the VM once before CI/CD wiring

Run:

```bash
cd /opt/hidden-adventures
docker compose config
docker compose up -d
docker compose ps
```

Why:

- The first successful boot should happen with the smallest possible moving surface.
- It is easier to debug Compose, env files, and host networking before GitHub Actions is involved.

### Phase 5: Automate image promotion and rollout

#### Step 12. Create the deploy script

Create `/opt/hidden-adventures/scripts/deploy.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

cd /opt/hidden-adventures

source .deploy.env

aws ecr get-login-password --region us-west-2 \
  | docker login --username AWS --password-stdin <account>.dkr.ecr.us-west-2.amazonaws.com

docker compose pull api admin
docker compose up -d
docker compose ps
```

Why:

- The host should pull exact promoted images rather than build them.
- A tiny deploy script keeps operator behavior repeatable and inspectable.

#### Step 13. Add deploy metadata tracking

- Extend `.deploy.env` to include:
  - registry URL
  - `API_IMAGE`
  - `ADMIN_IMAGE`
  - deploy region
- Record for every rollout:
  - date/time
  - operator
  - git SHA
  - image tag
  - image digest
  - migration result
  - smoke result
  - rollback target

Why:

- Digest-only rigor is hard to maintain if the deploy record is informal.
- Rollback confidence comes from knowing exactly what was running before the latest deploy.

#### Step 14. Decide how migrations run during deploy

- Prefer one explicit deploy-time migration step using the same promoted server image.
- Run migrations before final smoke approval.
- Treat migrations as forward-only unless a tested down path exists.

Why:

- This preserves the old deployment doc's strongest operational rule even though the runtime topology changed.
- Database rollback improvisation is usually the highest-risk part of incident response.

### Phase 6: Add smoke checks and operator diagnostics

#### Step 15. Create the smoke test script

Create `/opt/hidden-adventures/scripts/smoke.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

curl -fsS https://hiddenadventures.lucidios.com/api/health
curl -fsS https://hiddenadventures.lucidios.com/public/privacy-policy.html
curl -fsS https://hiddenadventures.lucidios.com/public/terms-conditions.html
```

Why:

- This gives a minimal cross-layer check of DNS, TLS, Caddy routing, app reachability, and static file serving.
- It is intentionally small so it can run after every deploy without noise.

#### Step 16. Standardize the first-line logs to inspect

- `docker compose logs -f api`
- `docker compose logs -f admin`
- `docker compose logs -f postgres`
- `sudo journalctl -u caddy -f`

Why:

- Operators need one agreed set of debugging entrypoints before production incidents happen.
- This preserves the useful observability baseline from the older deployment notes without requiring a full logging stack yet.

### Phase 7: Automate backups and document restore

#### Step 17. Create the Postgres backup script

Create `/opt/hidden-adventures/scripts/backup-postgres.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

DATE=$(date -u +"%Y-%m-%dT%H-%M-%SZ")
FILE="/opt/hidden-adventures/backups/db_$DATE.dump"

docker compose exec -T postgres \
  pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc > "$FILE"

aws s3 cp "$FILE" s3://<your-backup-bucket>/postgres/
```

Why:

- Co-locating Postgres with the app host is only acceptable if backups are automatic and off-box.
- Using `pg_dump -Fc` keeps the backup format practical for later targeted restore work.

#### Step 18. Schedule the daily backup job

Install a cron entry:

```cron
0 3 * * * /opt/hidden-adventures/scripts/backup-postgres.sh
```

Why:

- A backup that depends on a human remembering to run it is not a real backup policy.
- A single predictable daily run is enough for the first production baseline.

#### Step 19. Write and rehearse restore steps

- Document how to:
  - fetch the latest S3 dump
  - restore into a fresh Postgres container or replacement volume
  - verify the restored database
- Perform one dry run before calling production routine.

Why:

- Backup success without restore rehearsal creates false confidence.
- The earlier deployment doc correctly treated backup and restore as separate responsibilities.

### Phase 8: Wire GitHub Actions CI/CD

#### Step 20. Build and push production images in GitHub Actions

- Add one workflow that:
  - runs the relevant test suite
  - builds the API image
  - builds the admin image
  - pushes both to ECR
  - captures immutable digests

Why:

- CI should become the trusted producer of deployable artifacts.
- Capturing digests in CI avoids ambiguous "latest tag" promotion behavior.

#### Step 21. Choose the deploy trigger shape

- Prefer a manually approved production workflow first.
- Pass the exact promoted image refs to the VM deploy step.
- Keep automatic deploy-to-production disabled until the manual path is reliable.

Why:

- Manual approval is the safer default while the first rollout process is still being proven.
- This keeps CI/CD useful without forcing full autonomous production release behavior on day one.

#### Step 22. Connect CI output to VM rollout

- The deploy action should either:
  - SSH to the VM and update `.deploy.env`, then run `deploy.sh`
  - or write the promoted image refs into a known location the VM can consume
- Re-run `smoke.sh` immediately after deploy.

Why:

- The CI/CD handoff must update the host runtime definition, not leave operators to infer which image to pull.
- Immediate smoke checks turn deployment from "container started" into "service is actually reachable."

### Phase 9: Build the first admin console release

#### Step 23. Define the v1 admin scope

The first admin surface should show:

- total users
- new users
- total adventures
- visibility breakdown
- recent activity

Why:

- This is enough to validate the admin runtime path and give useful operator visibility.
- Keeping v1 intentionally small prevents the admin console from delaying the production baseline itself.

#### Step 24. Keep admin protection at the proxy layer first

- Protect `admin-adventures.lucidios.com` with Caddy basic auth.
- Add app-level auth later only if the console grows beyond a lightweight internal operator tool.

Why:

- Host-level auth is the fastest low-complexity protection that satisfies the current need.
- This avoids coupling production rollout to a brand-new internal auth system.

### Phase 10: Define rollout, rollback, and production-readiness gates

#### Step 25. Run the first end-to-end production rehearsal

- Pull real images from ECR.
- Bring up Compose on the VM.
- verify Caddy routing and HTTPS
- run smoke checks
- capture logs and runtime notes

Why:

- The first live rehearsal should validate the full chain, not isolated components.
- This is the point where the plan becomes an operating procedure instead of a design.

#### Step 26. Write the rollback checklist beside the deploy checklist

Rollback should be:

1. identify the last known-good image reference
2. restore `.deploy.env` or runtime image refs to that version
3. run `deploy.sh`
4. re-run `smoke.sh`
5. log the incident and follow-up actions

Why:

- Single-host deployments are only safe when rollback is explicit and short.
- Keeping rollback focused on image version change avoids unnecessary host drift during incidents.

#### Step 27. Mark production baseline complete only when these are true

- DNS resolves correctly for both domains
- Caddy serves valid HTTPS for both domains
- Compose restarts cleanly after host reboot
- API smoke checks pass
- legal static pages load publicly
- admin domain is protected and reachable
- CI builds and publishes immutable images
- production deploys use recorded image refs
- daily backups upload to S3 successfully
- one restore rehearsal has been completed

Why:

- Production readiness should be defined by proven behaviors, not by the existence of config files.

## Non-Goals

- Terraform
- Kubernetes
- managed Postgres for v1
- a separate load balancer tier
- Grafana or a broader observability platform for the first rollout
- a standing pre-production environment

## Recommended Execution Order

1. Confirm DNS, domains, ECR, S3, and IAM inputs.
2. Prepare the VM packages and directory layout.
3. Install static legal pages.
4. Configure and validate Caddy.
5. Create Compose and env files.
6. Boot the runtime manually on the VM once.
7. Add deploy and smoke scripts.
8. Add backup automation and restore notes.
9. Wire GitHub Actions build-and-push.
10. Connect CI deploy handoff to the VM.
11. Ship the v1 admin console.
12. Run the first production rehearsal and capture rollback notes.

## Done Means

- Hidden Adventures can be deployed to the existing Lightsail VM without manual image builds on the host.
- HTTPS, routing, and admin access control are handled by a stable host-level Caddy config.
- The public API and legal pages pass repeatable smoke checks after deploy.
- The database is backed up to S3 automatically and restore steps have been rehearsed.
- Operators have a concrete deploy log, rollback checklist, and first-line diagnostics path.
