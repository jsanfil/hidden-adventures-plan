# Feature: Ratings

## Summary

Allow users to rate adventures and display rating aggregates consistently on the surfaces that expose rating.

## Status

- Program status: `In Progress`
- Completion source of truth: this document

## Scope

- rating control on adventure detail
- current-user rating state
- displayed aggregate rating and count
- rating updates where the same user changes a prior rating

## Dependencies

- stable detail surface
- server-side aggregate or derived rating strategy

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [x] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- rating create or upsert endpoint
- rating aggregate inclusion in read models where needed

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [x] server tests added for rating mutation and aggregate behavior
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- Ratings should follow the rebuilt relational model rather than the legacy inline aggregate mutation approach.
- `hidden-adventures-server` now exposes `POST /api/adventures/:id/rating` and `DELETE /api/adventures/:id/rating`, and `GET /api/adventures/:id` now includes nullable `viewerRating` for the authenticated viewer only.
- Server aggregate refresh preserves imported legacy rating baseline through `public.adventure_stats` while layering rebuild-era per-user rows from `public.adventure_ratings` on top.
- Ratings remain incomplete at the feature level until accepted iOS integration and QA are recorded.

## Proof Links

- `hidden-adventures-server`: `docs/contract.md`
- `hidden-adventures-server`: `tests/adventures.routes.test.ts`
- `hidden-adventures-server`: `tests/adventures.repository.test.ts`
- `hidden-adventures-server`: `tests/app.test.ts`
- Verification: `npm test -- tests/adventures.repository.test.ts tests/adventures.routes.test.ts tests/app.test.ts`
- Verification: `npm test`
- Verification: `npm run check`
