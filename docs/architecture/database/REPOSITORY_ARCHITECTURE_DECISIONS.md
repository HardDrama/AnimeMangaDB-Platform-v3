# Repository Architecture Decisions

## Status

Updated for v0.5.9B.

## ADR-001 — Sessions are injected

Repositories receive an existing SQLAlchemy Session. They never construct or own one.

## ADR-002 — Callers own transactions

Repositories may add, delete, query, flush, and refresh. They never commit or roll back.

## ADR-003 — Repositories compose object graphs

Mappers remain shallow. Concrete repositories resolve ORM parents and reconstruct Domain parents before invoking child mappers.

## ADR-004 — Persistence identity remains internal

Database primary keys are not copied into Domain entities and are not required by public repository methods.

## ADR-005 — Public repository methods use Domain types

Public inputs and outputs use Domain entities and value objects. ORM rows do not cross the repository boundary.

## ADR-006 — Child title identity is parent-scoped

Anime and manga title lookup uses the parent Series slug plus the child slug or canonical title. This matches the composite uniqueness rules in persistence.

## ADR-007 — Parents must already be persistent

A child title cannot be staged unless its parent Series can be resolved in the current Session. Missing parents produce `LookupError` rather than silently creating a new aggregate.

## ADR-008 — Reads explicitly load required parents

Child repository queries eagerly load their Series relationship before graph composition. Repository results therefore do not depend on lazy loading after the Session boundary.
