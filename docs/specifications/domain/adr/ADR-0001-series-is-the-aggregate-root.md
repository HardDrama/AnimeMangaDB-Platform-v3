# ADR-0001 — Series Is the Aggregate Root

## Status

Accepted

## Context

AnimeMangaDB must support properties containing multiple anime adaptations and multiple manga publications. Using either branch as the root would make the sibling branch secondary or indirectly owned.

## Decision

`Series` is the aggregate root. Anime Titles and Manga Titles belong directly to one Series. Episodes belong to Anime Titles. Chapters belong to Manga Titles.

## Consequences

### Positive

- Multiple adaptations and publications fit naturally.
- Series-level browsing is unambiguous.
- Future remakes do not require restructuring.

### Negative

- Some queries require traversal from Series to a child title.
- Series identity must exist before child titles are created.

## Rules established

- Every Anime Title belongs to exactly one Series.
- Every Manga Title belongs to exactly one Series.
- Series identity is independent of any one adaptation.
