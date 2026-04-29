# Feature: Comments

## Summary

Add visible comment threads and comment creation on adventure detail while preserving visibility and author identity rules.

## Status

- Program status: `In Progress`
- Completion source of truth: this document

## Scope

- comment list on adventure detail
- comment composer
- empty, loading, and error states
- comment author identity display
- visibility-aware comment read and write behavior

## Dependencies

- stable adventure detail surface
- viewer identity and profile data

## Delivery Gates

- [ ] Design accepted
- [ ] Mock iOS accepted
- [x] Server accepted
- [ ] Integrated iOS accepted
- [ ] QA accepted

## Public Interface Expectations

- comment list read support
- comment create endpoint
- visibility enforcement for both reads and writes

## QA And Proof

- [ ] v0 screenshots and UX notes linked
- [ ] SwiftUI gallery coverage updated
- [x] server tests added for comment reads and writes
- [ ] integrated local happy path validated
- [ ] manual QA notes recorded

## Notes

- Comment presentation should use current profile state rather than denormalized snapshots where possible.
- Server support is implemented in `hidden-adventures-server` for `GET /api/adventures/:id/comments` and `POST /api/adventures/:id/comments`, including visibility checks, completed-local-account enforcement for writes, current profile-backed author fields, and `adventure_stats.comment_count` refresh on create.

## Proof Links

- `hidden-adventures-server`: `docs/contract.md`
- `hidden-adventures-server`: `tests/adventures.routes.test.ts`
- `hidden-adventures-server`: `tests/adventures.repository.test.ts`
- Verification: `npm run check`; `npm test`
