# Legacy Mongo Archive Profile

## Source

- Archive: `hidden-adventures-plan/migration/archives/legacy-mongodb-backup-2026-03-01.archive`
- Size: `1263783` bytes
- Tool version: `r3.6.5`
- Server version: `3.6.5`
- Concurrent collections setting: `4`

## Collection Counts

| Collection | Documents | Indexes | Index Names |
| --- | --- | --- | --- |
| adventures | 353 | 6 | _id_, location, access, acl, author, category |
| comments | 145 | 3 | _id_, username, adventureID_1 |
| favorites | 1958 | 2 | _id_, username |
| filenames | 0 | 1 | _id_ |
| messages | 0 | 1 | _id_ |
| profiles | 2630 | 2 | _id_, username |
| sidekicks | 1190 | 2 | _id_, username |

## Key Findings

- `ratings` is not present in the archive metadata or data segments.
- Adventure documents still include `rating` and `ratingCount`, and the legacy app displayed the average as `rating / ratingCount`.
- `messages` and `filenames` exist as collections but currently contain `0` documents in this archive.
- `adventures` contains `353` records, with `1` authors missing a matching profile row.
- `favorites` contains `1958` records, including `61` references to missing adventures.
- `comments` contains `145` records, including `3` references to missing adventures.
- `sidekicks` contains `1190` records, with `24` links that reference a missing profile on one side.
- `defaultImage` is the real legacy image model for adventures; `images[]` was not fully implemented in the shipped product.

## Adventure Access Distribution

| Access | Count |
| --- | --- |
| Public | 298 |
| Private | 30 |
| Sidekicks | 25 |

## Adventure Category Distribution

| Category | Count |
| --- | --- |
| Viewpoint | 87 |
| Trail | 63 |
| Restaurant | 33 |
| Abandoned | 25 |
| Beach_Cove | 21 |
| Cafe | 18 |
| Cave | 16 |
| Creek_Rivers | 14 |
| Forest | 13 |
| RopeSwing | 12 |
| road | 10 |
| Bar | 10 |
| SwimmingHole | 9 |
| LiveMusic | 9 |
| Bridge | 8 |
| Desert | 3 |
| Fishing | 2 |

## Migration Risk Notes

- Every adventure has location data in this archive. The migration should treat `defaultImage` as the authoritative adventure image because multi-image support was not implemented in the legacy product.
- Rating migration should treat `adventures.rating` as the accumulated score total and `adventures.ratingCount` as the divisor for the displayed average.
- `4` `Sidekicks` adventures have no ACL payload, so visibility conversion should not assume `access = Sidekicks` guarantees a complete allowed-viewer list.
- `1788` profiles are missing `profileImage`, so the rebuild should expect sparse avatar coverage during migration.
- Orphaned favorites and comments should be deleted during migration rather than preserved as dangling references.
