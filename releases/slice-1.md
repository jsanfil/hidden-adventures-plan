# Slice 1: Hardening And Integration

## Scope

- auth bootstrap and public-handle selection
- profile bootstrap entry path
- explore shell with feed and map modes
- adventure detail
- image delivery references
- manual authenticated API troubleshooting requests kept in sync with the live server surface

## Current Status

- visual exploration exists in `v0-hidden-adventures-ui`
- native SwiftUI shell exists in `hidden-adventures-ios`, and the default runtime now targets the live Slice 1 server surface
- local server endpoints exist for auth bootstrap, handle selection, feed, detail, and profile
- contract notes and Postman troubleshooting requests exist for the implemented Slice 1 surface
- non-production server auth now uses seeded local bearer tokens for repeatable Slice 1 verification without Cognito
- deployment baseline docs, env templates, and staging smoke script exist in `hidden-adventures-server/deploy/`
- migration-backed local data is published and testable
- the deterministic UI harness still runs in explicit fixture-preview mode, so live-runtime acceptance remains a separate final check

## Acceptance Criteria

- [x] server exposes `GET /api/auth/bootstrap`
- [x] server exposes `POST /api/auth/handle`
- [x] server exposes `GET /api/feed`
- [x] server exposes `GET /api/adventures/:id`
- [x] server exposes `GET /api/profiles/:handle`
- [x] server tests cover authenticated viewer resolution without `viewerHandle`
- [x] native Slice 1 shell exists with deterministic UI harness coverage
- [x] Slice 1 contracts are documented from real payloads and auth expectations
- [x] Postman assets model authenticated viewer behavior instead of `viewerHandle`
- [x] iOS uses real network services and auth bootstrap for Slice 1 flows
- [ ] local happy path works end to end across auth bootstrap, feed, detail, and profile

## Missing Gaps

- the passing iOS UI gallery and walkthrough still exercise fixture-preview mode rather than the live server runtime
- live Slice 1 keeps a few explicit temporary fallbacks: handle-only profile setup, feed-derived map cards, and placeholder media until later contracts lock
- the local live-runtime happy path has not yet been explicitly re-run end to end in this planning cycle
- the deployment baseline exists, but its staging smoke path has not yet been executed against a real staging host

## Current Server Contract

### Auth model

- `GET /api/health` is the only public Slice 1 route
- `GET /api/auth/bootstrap`, `POST /api/auth/handle`, `GET /api/feed`, `GET /api/adventures/:id`, and `GET /api/profiles/:handle` all require `Authorization: Bearer <token>`
- non-production defaults to `AUTH_MODE=local_identity`, which accepts seeded local tokens such as `local:connected_viewer`, `local:non_connected_viewer`, and `local:new_user`
- production must run with `AUTH_MODE=cognito`
- protected routes return `401` with `{ "error": "Authentication required." }` when no authenticated identity is present
- invalid bearer tokens return `401` with `{ "error": "Invalid authentication token." }`
- `viewerHandle` is not part of the public request contract

### Endpoint notes

- `GET /api/auth/bootstrap`
  returns `accountState`, `user`, `suggestedHandle`, and `recoveryEmail`
  current account states are `linked`, `legacy_claimed`, `new_user_needs_handle`, and `manual_recovery_required`
- `POST /api/auth/handle`
  accepts `{ "handle": string }`
  validates `handle` as 3-64 trimmed characters matching `[A-Za-z0-9_]+`
  normalizes the stored handle to lowercase before creating a rebuild user
  returns the same bootstrap-style account payload on success
  returns `409` when the requested handle is unavailable
- `GET /api/feed`
  returns `{ items, paging }`
  requires auth
  accepts only `limit` and `offset`; unknown query params like `viewerHandle` return `400`
- `GET /api/adventures/:id`
  returns `{ item }`
  requires auth
  accepts no query params; `viewerHandle` returns `400`
  returns `404` when the adventure is not visible or does not exist
- `GET /api/profiles/:handle`
  returns `{ profile, adventures, paging }`
  requires auth
  accepts only `limit` and `offset`; unknown query params like `viewerHandle` return `400`
  returns `404` when the handle is unknown

### Locked planning assumptions

- profile lookup is public-handle based
- authenticated viewer identity is local `users.id` resolved from auth context, with Cognito in production and seeded local identities in non-production
- Vitest is the official server verification suite
- Postman is a manual troubleshooting surface that should stay current with the live API, not a formal acceptance runner
- the checked-in troubleshooting requests live under `hidden-adventures-api-tests/postman/collections/hidden-adventures-slice-1/`
- the server-side contract handoff lives in `hidden-adventures-server/docs/slice-1-contract.md`

## Local Test Checklist

- [x] `hidden-adventures-server`: `npm test`
- [x] `hidden-adventures-server`: `npm run check`
- [x] `hidden-adventures-ios`: simulator build and UI test bundle succeed via `Scripts/run_ui_gallery.sh`
- [x] `hidden-adventures-ios`: `Scripts/run_ui_gallery.sh` still passes after real API wiring
- [ ] optional manual Postman check: `GET /api/auth/bootstrap` succeeds with `Authorization: Bearer {{newUserToken}}`
- [ ] optional manual Postman check: `GET /api/feed` returns connected-viewer data with `Authorization: Bearer {{connectedViewerToken}}`
- [ ] optional manual Postman check: `GET /api/adventures/:id` returns the connections path with `Authorization: Bearer {{connectedViewerToken}}`
- [ ] optional manual Postman check: `GET /api/profiles/:handle` resolves by handle with `Authorization: Bearer {{connectedViewerToken}}`
- [ ] explicit live-app check: run the iOS app in live mode against the local server with `HA_TEST_AUTH_TOKEN=local:connected_viewer`
- [ ] explicit live-app check: run the bootstrap and handle-selection flow with `HA_TEST_AUTH_TOKEN=local:new_user`

## Staging Validation Checklist

- [x] staging runtime shape documented
- [ ] auth bootstrap smoke-tested in staging
- [ ] read-only Slice 1 routes smoke-tested in staging
- [ ] logs checked for auth or visibility regressions

## Migration Impact

- none for active implementation
- use the published migration dataset and reconciliation artifacts as the Slice 1 local truth source

## Rollback Notes

- iOS integration rollback should preserve the explicit fixture-preview UI path until live-runtime acceptance is verified
- server contract changes should remain additive or be guarded until the iOS integration thread is complete
- deploy rollback should prefer the last known good image digest; database rollback should stay exceptional and forward-fix oriented
