# Cognito Account Linking Findings

## Goal

Capture the proven legacy identity behavior, the live Cognito pool findings, and the resulting implementation rules for the rebuild.

## What We Verified

### Legacy mobile identity model

- The shipped iOS client used Cognito `username` as the authenticated identity key.
- Legacy sign-up sent the typed username directly to Cognito and also copied that same value into the profile model before the profile was posted to the server.
- The client stored pending profiles under the username key locally and posted them after first successful login using the current Cognito username.
- The app consistently used the current Cognito username for profile lookup, authorship, comments, favorites, sidekicks, and delete-account routes.
- We did not find a client-side flow that changed `profile.username` after sign-up.

Conclusion:

- The intended legacy linkage is `Cognito username == legacy profile username`.
- In the rebuild relational schema, that means `Cognito username == users.handle` for imported users.

## Live Cognito Pool Findings

- User pool: `us-west-2_xCoWAVG4i`
- Pool name: `Adventurers`
- Region: `us-west-2`
- Email is an alias attribute and is required and auto-verified.
- The current legacy app client supports password-era flows and does not currently have OAuth/social federation enabled.
- The pool contains materially more users than the legacy published profile set, including abandoned or incomplete accounts created after the original app era.

## Migration Dataset Findings

After publishing import run `2` into the rebuild `public` tables and reconciling against the live Cognito pool:

- Total legacy-backed app users/profiles in the local rebuild DB: `2598`
- Total Cognito users in the live pool: `3981`
- Exact-handle Cognito matches to legacy `users.handle`: `2598`
- Cognito accounts with no legacy profile match: `1383`

This is the most important result:

- every imported legacy profile currently published in the rebuild DB has an exact Cognito username match
- therefore bulk migration linking should be driven by exact handle only

## Duplicate and Noise Findings

During review we found several kinds of bad or non-authoritative records:

- Cognito users that never had a published legacy profile
- duplicate Cognito accounts for the same email/person
- zero-activity duplicate legacy profiles in the local rebuild DB

What we did in the local migration environment:

- removed `29` zero-activity duplicate local legacy profiles so they no longer participate in migration
- reset `15` manually linked `cognito_subject` assignments after confirming they were not canonical
- reran the bulk mapping from a clean state

## Final Bulk-Linking Rule

For migration-time bulk reconciliation:

1. if `users.cognito_subject` already matches the Cognito `sub`, keep it
2. otherwise link only when exact `Cognito Username == users.handle`
3. skip everything else

Explicit non-rules for bulk reconciliation:

- do not bulk auto-link by email
- do not create a `public.users` row for a Cognito account that lacks a legacy profile
- do not trust extra Cognito accounts that share an email with a linked legacy user

Rationale:

- the legacy product identity bridge was username-first
- the live pool contains duplicate and abandoned Cognito accounts
- exact-handle bulk linking yields a complete `2598 / 2598` mapping for legacy profiles without needing email heuristics

## Runtime Claim and New-User Rules

Bulk migration and runtime account recovery are different concerns.

Bulk migration:

- exact handle only

Runtime legacy recovery:

- allow verified-email claim flow for a returning user who cannot remember username or password
- email-based recovery should bind only after interactive verification and only when the result is safe

New user creation:

- do not infer a legacy profile from bulk Cognito presence alone
- if no legacy profile is reclaimed, create a fresh rebuild user
- require the user to choose a public `handle` during onboarding

## Current Local Applied State

The local rebuild DB is now in the desired migration posture:

- `2598` DB users
- `2598` DB profiles
- `2598` linked `cognito_subject` values
- `0` unlinked imported legacy profiles
- `0` duplicate `cognito_subject` groups

The post-apply sync is stable:

- `already_linked_by_cognito_subject`: `2598`
- `skipped_no_legacy_profile_match`: `1383`

## Follow-On Implementation Guidance

- Preserve `handle` as the public app alias, not the long-term login identifier.
- Keep email-based legacy recovery in the runtime bootstrap/claim flow, not in the bulk sync job.
- Keep Cognito as the identity provider, but treat the rebuild backend `users` row as the authoritative application identity record.
- Extend Cognito for Apple/Google in a new or updated rebuild app client rather than rewriting the legacy identity history.

## Artifacts

- Unmatched Cognito account list:
  `migration/reports/cognito-unmatched-users-2026-03-28.json`
- CSV companion:
  `migration/reports/cognito-unmatched-users-2026-03-28.csv`
