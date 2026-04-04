# Slice 1: Hardening And Integration

## Scope

- email OTP auth entry
- auth bootstrap and public-handle selection
- new-user onboarding and profile bootstrap entry path
- explore shell with feed and map modes
- adventure detail
- image delivery references
- manual authenticated API troubleshooting requests kept in sync with the live server surface

## Current Status

- visual exploration exists in `v0-hidden-adventures-ui`
- native SwiftUI shell exists in `hidden-adventures-ios`, and the default runtime now targets the live Slice 1 server surface
- local server endpoints exist for auth bootstrap, handle selection, viewer profile read/write, feed, detail, and public profile
- contract notes and Postman troubleshooting requests exist for the implemented Slice 1 surface
- local automation still uses deterministic signed test JWTs for repeatable Slice 1 verification
- local manual QA and production auth now target real Cognito email OTP flows
- deployment baseline docs, env templates, and staging smoke script exist in `hidden-adventures-server/deploy/`
- migration-backed local data is published and testable
- the deterministic UI harness still runs in explicit fixture-preview mode, so live-runtime acceptance remains a separate final check
- the program is now in Slice 1 acceptance-closure mode; Slice 2 stays definition-only until the live local checks below are closed

## Acceptance Criteria

- [x] server exposes `GET /api/auth/bootstrap`
- [x] server exposes `POST /api/auth/handle`
- [x] server exposes `GET /api/feed`
- [x] server exposes `GET /api/adventures/:id`
- [x] server exposes `GET /api/adventures/:id/media`
- [x] server exposes `GET /api/media/:id`
- [x] server exposes `GET /api/profiles/:handle`
- [x] server exposes `GET /api/me/profile` and `PUT /api/me/profile`
- [x] server tests cover authenticated viewer resolution without `viewerHandle`
- [x] native Slice 1 shell exists with deterministic UI harness coverage
- [x] Slice 1 contracts are documented from real payloads and auth expectations
- [x] Postman assets model authenticated viewer behavior instead of `viewerHandle`
- [x] iOS uses real network services, native email OTP auth, and auth bootstrap for Slice 1 flows
- [ ] local happy path works end to end across email OTP auth entry, auth bootstrap, onboarding, feed, detail, and profile

## Missing Gaps

- the passing iOS UI gallery and walkthrough still exercise fixture-preview mode rather than the live server runtime
- live Slice 1 still keeps an explicit temporary fallback for feed-derived map cards until a locked map contract exists
- the local live-runtime happy path has not yet been explicitly re-run end to end for both new-user onboarding and linked-user direct sign-in in this planning cycle
- the deployment baseline exists, but its staging smoke path has not yet been executed against a real staging host
- Postman remains a manual troubleshooting path only and does not close Slice 1 acceptance on its own

## Current Server Contract

### Auth model

- `GET /api/health` is the only public Slice 1 route
- `GET /api/auth/bootstrap`, `POST /api/auth/handle`, `GET /api/me/profile`, `PUT /api/me/profile`, `GET /api/feed`, `GET /api/adventures/:id`, `GET /api/adventures/:id/media`, `GET /api/media/:id`, and `GET /api/profiles/:handle` all require `Authorization: Bearer <token>`
- the rebuild app should expose one visible email OTP entry path for both `Get Started` and `Sign In`
- local automation uses deterministic signed test JWTs for integration and regression work
- local manual QA and production use Cognito-backed email OTP auth
- production must run with `AUTH_MODE=cognito`
- protected routes return `401` with `{ "error": "Authentication required." }` when no authenticated identity is present
- invalid bearer tokens return `401` with `{ "error": "Invalid authentication token." }`
- `viewerHandle` is not part of the public request contract

### Endpoint notes

- `GET /api/auth/bootstrap`
  returns `accountState`, `user`, `suggestedHandle`, and `recoveryEmail`
  the supported app behavior should effectively collapse to `linked` for existing mapped users and `new_user_needs_handle` for brand-new users
  any `manual_recovery_required` result should now be treated as an operational or data-quality defect, not a planned user-facing branch
- `POST /api/auth/handle`
  accepts `{ "handle": string }`
  validates `handle` as 3-64 trimmed characters matching `[A-Za-z0-9_]+`
  normalizes the stored handle to lowercase before creating a rebuild user
  returns the same bootstrap-style account payload on success
  returns `409` when the requested handle is unavailable
- `GET /api/me/profile`
  returns `{ profile }`
  requires auth
  mirrors the `profile` object shape used by `GET /api/profiles/:handle`
- `PUT /api/me/profile`
  accepts `{ "displayName": string | null, "bio": string | null, "homeCity": string | null, "homeRegion": string | null }`
  trims strings, normalizes empty values to `null`, and creates the profile row on first write when needed
  returns `{ profile }` with the saved viewer profile payload
- `GET /api/feed`
  returns `{ items, paging }`
  requires auth
  accepts only `limit` and `offset`; unknown query params like `viewerHandle` return `400`
- `GET /api/adventures/:id`
  returns `{ item }`
  requires auth
  accepts no query params; `viewerHandle` returns `400`
  returns `404` when the adventure is not visible or does not exist
- `GET /api/adventures/:id/media`
  returns `{ items }`
  requires auth
  returns ordered media refs for the visible adventure detail carousel
  returns `404` when the adventure is not visible or does not exist
- `GET /api/media/:id`
  returns authenticated image bytes for a visible adventure media id
  requires auth
  the app should use media ids for delivery and not treat `storageKey` as a URL
- `GET /api/profiles/:handle`
  returns `{ profile, adventures, paging }`
  requires auth
  accepts only `limit` and `offset`; unknown query params like `viewerHandle` return `400`
  returns `404` when the handle is unknown

### Locked planning assumptions

- profile lookup is public-handle based
- authenticated viewer identity is local `users.id` resolved from auth context, with Cognito in production and seeded local identities in non-production
- `Get Started` and `Sign In` share one auth mechanism, but onboarding should continue only for users who authenticate and then bootstrap as `new_user_needs_handle`
- linked legacy users and linked rebuild users should skip onboarding/profile setup and land directly in Explore/Feed
- persisted sessions should relaunch directly into Explore/Feed until logout clears local auth state
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
- [ ] explicit live-app check: `Get Started` -> email OTP -> `new_user_needs_handle` -> handle selection -> profile setup -> Feed
- [ ] explicit live-app check: `Sign In` -> email OTP -> linked user -> Feed
- [ ] explicit live-app check: relaunch with persisted authenticated session -> direct Feed
- [ ] explicit live-app check: logout -> next entry requires email OTP again

Completion note:

- Slice 1 acceptance should not be marked complete until the explicit live-app checks above are done against a running local server and the fallback inventory is reconfirmed, including the onboarding-versus-linked routing split.

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
