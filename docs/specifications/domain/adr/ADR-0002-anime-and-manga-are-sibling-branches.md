# ADR-0002 — Anime and Manga Are Sibling Branches

## Status

Accepted

## Context

The legacy platform allowed anime and manga concerns to become coupled through repositories and navigation paths, making ownership unclear and creating cyclic dependencies.

## Decision

Anime and manga are sibling branches under Series.

```text
Series
├── Anime Titles
└── Manga Titles
```

Neither branch owns the other.

## Consequences

### Positive

- Anime and manga persistence remain separate.
- Branches can evolve independently.
- Multiple titles on either side are supported.
- The ownership tree remains acyclic.

### Negative

- Cross-branch queries require service orchestration.
- Adaptation relationships require a separate mapping model.

## Rules established

- Anime Title owns Episodes.
- Manga Title owns Chapters.
- Cross-branch behavior belongs to mappings and services.
