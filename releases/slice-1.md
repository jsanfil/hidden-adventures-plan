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
- native SwiftUI shell exists in `hidden-adventures-ios`
- local server endpoints exist for auth bootstrap, handle selection, feed, detail, and profile
- migration-backed local data is published and testable
- the slice is not yet end to end because the iOS app is still fixture-backed

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
- [ ] iOS uses real network services and auth bootstrap for Slice 1 flows
- [ ] local happy path works end to end across auth bootstrap, feed, detail, and profile

## Missing Gaps

- the iOS client still uses fixture-backed services and a fixture-backed viewer identity
- staging and rollback checks do not yet exist for the slice

## Current Server Contract

### Auth model

- `GET /api/auth/bootstrap` requires `Authorization: Bearer <Cognito ID token>`
- `POST /api/auth/handle` requires `Authorization: Bearer <Cognito ID token>`
- `GET /api/feed`, `GET /api/adventures/:id`, and `GET /api/profiles/:handle` support unauthenticated public reads, but connected-viewer visibility now comes only from authenticated auth context
- `viewerHandle` is not part of the public request contract

### Endpoint notes

- `GET /api/auth/bootstrap`
  returns `accountState`, `user`, `suggestedHandle`, and `recoveryEmail`
- `POST /api/auth/handle`
  accepts `{ "handle": string }`
  returns the same bootstrap-style account payload on success
  returns `409` when the requested handle is unavailable
- `GET /api/feed`
  returns `{ items, paging }`
- `GET /api/adventures/:id`
  returns `{ item }`
  returns `404` when the adventure is not visible or does not exist
- `GET /api/profiles/:handle`
  returns `{ profile, adventures, paging }`
  returns `404` when the handle is unknown

### Locked planning assumptions

- profile lookup is public-handle based
- authenticated viewer identity is local `users.id` resolved from Cognito-backed auth context
- Vitest is the official server verification suite
- Postman is a manual troubleshooting surface that should stay current with the live API, not a formal acceptance runner

## Local Test Checklist

- [x] `hidden-adventures-server`: `npm test`
- [x] `hidden-adventures-server`: `npm run check`
- [ ] optional manual Postman check: authenticated `GET /api/auth/bootstrap` succeeds with a valid local Cognito token
- [ ] optional manual Postman check: authenticated `GET /api/feed` returns connected-viewer data without `viewerHandle`
- [ ] optional manual Postman check: authenticated `GET /api/adventures/:id` returns the connected-viewer detail path without `viewerHandle`
- [ ] optional manual Postman check: authenticated `GET /api/profiles/:handle` resolves by handle with viewer-aware visibility
- [ ] `hidden-adventures-ios`: simulator build succeeds against the current app target
- [ ] `hidden-adventures-ios`: `Scripts/run_ui_gallery.sh` still passes after real API wiring

## Staging Validation Checklist

- [ ] staging runtime shape documented
- [ ] auth bootstrap smoke-tested in staging
- [ ] read-only Slice 1 routes smoke-tested in staging
- [ ] logs checked for auth or visibility regressions

## Migration Impact

- none for active implementation
- use the published migration dataset and reconciliation artifacts as the Slice 1 local truth source

## Rollback Notes

- iOS integration rollback should preserve the existing fixture-backed UI path until real integration is verified
- server contract changes should remain additive or be guarded until the iOS integration thread is complete
- staging rollback path is pending deployment-baseline work
