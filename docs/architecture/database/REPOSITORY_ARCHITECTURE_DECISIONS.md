# Repository Architecture Decisions

Version: v0.5.9C

## ADR-001 — Sessions are injected

Repositories receive a caller-owned SQLAlchemy Session.

## ADR-002 — Callers own transactions

Repositories never commit, roll back, or close Sessions.

## ADR-003 — Mappers remain shallow

Mappers convert one entity at a time and receive already-resolved parents or related objects.

## ADR-004 — Repositories compose object graphs

Title repositories compose Series parents. Installment repositories extend this rule by composing Series → Title → Installment graphs. Mapping repositories compose both branches.

## ADR-005 — Persistence identity remains internal

Database primary keys do not enter Domain entities or public repository APIs.

## ADR-006 — Installment identifiers remain strings

Repositories preserve `InstallmentIdentifier.value` exactly. They do not parse, normalize, or numerically sort identifiers.

## ADR-007 — Installment identity is parent-scoped

An episode is identified by Series, AnimeTitle, and installment identifier. A chapter is identified by Series, MangaTitle, and installment identifier. This mirrors the ORM uniqueness constraints without exposing database IDs.

## ADR-008 — Mapping identity is relational

An EpisodeChapterMapping is identified by its resolved Episode and Chapter pair. The repository enforces this through Domain relationships and the database unique constraint.

## ADR-009 — Public generic CRUD is avoided

Concrete repositories expose business-specific operations rather than a public infrastructure-oriented CRUD surface.
