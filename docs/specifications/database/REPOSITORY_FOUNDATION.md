# Repository Foundation

## Scope

v0.5.9A establishes the shared infrastructure used by concrete
SQLAlchemy repositories.

It does not implement Series, title, installment, or mapping
repositories. Those are introduced by later v0.5.9 packages.

## Dependency Direction

```text
Application / API
        ↓
Concrete Repository
        ↓
Entity Mapper
        ↓
SQLAlchemy ORM
        ↓
Database
```

Domain entities do not import repositories, SQLAlchemy, Sessions,
ORM models, or persistence identities.

## Session Injection

Every repository receives an already-created SQLAlchemy `Session`.

```python
repository = SeriesRepository(session)
```

A repository does not create its own engine or Session. This keeps
connection and transaction ownership at the application boundary.

## Transaction Ownership

Repositories may:

- execute queries;
- stage additions;
- stage deletions;
- flush pending changes;
- refresh persisted objects.

Repositories must not:

- commit;
- roll back;
- close the Session;
- open a replacement Session.

The caller decides whether a complete use case succeeds and commits
or fails and rolls back.

## Protected Foundation Operations

`Repository` provides protected helpers for concrete repositories:

- `_add`
- `_delete`
- `_flush`
- `_refresh`
- `_get_by_persistence_id`
- `_one_or_none`
- `_list`
- `_exists`

They are protected because API and application code should interact
with explicit business-facing methods such as `get_by_slug`,
`get_by_identifier`, or `create`.

## Persistence Identity

`_get_by_persistence_id` exists for repository-internal graph
composition and relationship resolution.

Persistence IDs remain infrastructure concerns. Concrete repository
methods return Domain entities rather than exposing IDs or ORM
objects to API callers.

## Mapper Integration

The base repository deliberately does not know which mapper applies
to a model. Concrete repositories select and invoke their specific
mapper while resolving any required parent objects.

This preserves:

- shallow mapper behavior;
- repository-owned graph composition;
- explicit query behavior;
- testable transaction boundaries.

## List Semantics

`_list` returns a new Python list on every invocation. Ordering is
chosen explicitly by each concrete repository statement.

The base class does not invent a universal ordering policy.

## Error Semantics

The foundation does not translate database integrity exceptions.
Concrete repository packages will define operation-specific behavior
only after their real query and persistence requirements are known.
