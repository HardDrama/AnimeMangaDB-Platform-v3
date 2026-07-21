# ADR-0003 — Episode-Chapter Links Use Explicit Mappings

## Status

Accepted

## Context

Episodes and Chapters have a many-to-many adaptation relationship. Treating either endpoint as owner of the other creates recursive ownership and repository coupling.

## Decision

Every Episode-to-Chapter relationship is represented by an explicit `EpisodeChapterMapping`.

```text
Episode ── EpisodeChapterMapping ── Chapter
```

The mapping references both endpoints and owns only relationship metadata.

## Consequences

### Positive

- Many-to-many adaptation is explicit.
- Relationship metadata has a clear owner.
- Both navigation directions remain safe.
- Duplicate relationships can be constrained.

### Negative

- Queries must join through the mapping entity.
- Mapping lifecycle must be handled explicitly.

## Rules established

- A mapping references exactly one Episode and one Chapter.
- A mapping owns neither endpoint.
- Duplicate Episode-Chapter pairs are forbidden.
- Initial Platform v3 mappings remain within one Series.
