# Workstream: Testing and Environments

## Summary

This document is the cross-repo source of truth for local testing, fixture data, environment separation, and deployment assumptions.

The rebuild now uses:

- two environments: `local` and `production`
- two local runtime modes:
  - `local-manual-qa`
  - `local-automation-test-core`
- one local Postgres container with two logical databases:
  - `hidden_adventures_qa`
  - `hidden_adventures_test`
- manifest-driven fixture packs:
  - `qa-rich`
  - `test-core`

## Local Environment Assumptions

### Laptop Runtime Shape

- the iOS app runs locally in Xcode, Simulator, or on a device
- the server runs locally from the sibling `hidden-adventures-server` repo
- PostgreSQL runs locally in Docker
- one Postgres instance hosts two logical databases:
  - `hidden_adventures_qa`
  - `hidden_adventures_test`
- AWS services are real but non-production:
  - a dedicated non-prod Cognito pool and app client for manual QA
  - a dedicated non-prod S3 bucket for fixture media

### Local Mode Split

#### `local-manual-qa`

- database: `hidden_adventures_qa`
- fixture pack: `qa-rich`
- auth: real Cognito email OTP
- media: real non-prod S3
- iOS scheme: `HiddenAdventures-LocalManualQA`
- server env file: `.env.local.manual-qa`
- primary use: backend preparation for interactive mobile-app testing and production-like email-code login or account creation

#### `local-automation-test-core`

- database: `hidden_adventures_test`
- fixture pack: `test-core`
- auth: deterministic signed test JWTs
- media: real non-prod S3 references used by the test pack
- iOS scheme: `HiddenAdventures-LocalAutomation`
- server env file: `.env.local.automation`
- primary use: repeatable server regression, client regression, and integration automation

## Mode and Configuration Rules

- `qa-rich` and `test-core` do not share the same logical database
- the server switches modes by env file, not by manual variable edits
- the iOS app switches modes by Xcode scheme, not by hand-editing build settings
- local manual QA and local automation can share the same Postgres container and the same non-prod S3 bucket, but not the same local database
- fixture preview remains an iOS-only UI harness mode and is separate from server environment selection

## Fixture System

### Canonical Source

- test data lives in versioned metadata manifests inside `hidden-adventures-server`
- fixture data does not live inside server auth source files anymore
- deterministic IDs are derived from stable manifest keys so reseeding reproduces the same rows

### Fixture Packs

#### `qa-rich`

- curated, visually rich dataset for interactive testing
- includes linked personas, rich profiles, connections, public and gated adventures, and representative engagement
- manual testers can extend it by editing manifests and adding media objects to the non-prod S3 bucket

#### `test-core`

- intentionally smaller, faster, and deterministic dataset for regression suites
- supports linked and unlinked personas so bootstrap and handle-selection flows can be exercised without Cognito

## Data Lifecycle

### Local `hidden_adventures_qa`

- seeded from `qa-rich`
- reseed before a formal manual QA pass
- reseed after write-heavy exploratory sessions when the baseline matters
- reseed after fixture-manifest or schema changes
- may stay populated between manual QA sessions if preserving state is useful

### Local `hidden_adventures_test`

- seeded from `test-core`
- reset and reseed before automated regression runs
- treated as disposable and reproducible
- should not be used as a long-lived exploratory dataset

### Production

- production uses live user data only
- no fixture seeding and no destructive refreshes
- schema changes land through forward migrations
- backups and restore procedures belong to the production operations workflow

## AWS Resource Assumptions

### Local Non-Prod Resources

- dedicated non-prod Cognito pool and app client for manual QA
- QA personas should have usable verified email addresses so OTP delivery can be exercised during local manual QA
- dedicated non-prod S3 bucket for local fixture media
- no sharing of production Cognito or production S3 with local manual QA

### Production Resources

- production Cognito pool and app client remain separate from local manual QA
- production S3 bucket remains separate from local manual QA
- the production database is external to the app container
- production is not the main QA environment

## Lightsail Deployment Assumptions

- the production deployment target is an AWS Lightsail VM
- the deployable unit is an immutable Docker image, not a running container copied from another host
- images should be built from the repo and pushed to a registry, preferably ECR
- the Lightsail host should pull by image digest and restart the server container from that digest
- PostgreSQL is external to the app container
- Cognito and S3 stay as AWS-managed services outside Lightsail
- there is no required dedicated staging environment in this phase; local validation is the main non-production acceptance path

## Mobile App Manual QA Backend Prep

1. Start the local Postgres container.
2. Create or migrate `hidden_adventures_qa`.
3. Validate the `qa-rich` fixture pack.
4. Verify the referenced S3 media objects.
5. Provision or reconcile the QA personas in the non-prod Cognito pool.
6. Seed `hidden_adventures_qa` from `qa-rich`.
7. Start the server with `npm run dev:manual-qa`.
8. Launch the iOS app with `HiddenAdventures-LocalManualQA`.
9. Validate OTP delivery and sign in with a linked QA persona through the real Cognito email-code flow.
10. Validate the new-user path through `Get Started`, including handle selection and onboarding routing.
11. Reseed the QA database whenever a clean baseline is needed.

This workflow is for preparing a realistic backend for manual mobile-app testing. Automated server verification belongs to the `test-core` regression lane.

## Adding More Test Data

1. Edit the fixture manifest for the appropriate pack.
2. Upload any new media assets to the non-prod S3 bucket.
3. Re-run fixture validation.
4. Re-run media verification.
5. Re-seed the target local database.
6. Re-run Cognito provisioning if QA personas changed.

## Cross-Repo Responsibilities

- `hidden-adventures-server` owns fixture manifests, seeding, auth modes, env files, and local DB tooling
- `hidden-adventures-ios` owns runtime selection, Xcode schemes, and documented manual QA versus automation behavior
- `hidden-adventures-plan` owns the global operating model, acceptance expectations, and cross-repo environment truth
