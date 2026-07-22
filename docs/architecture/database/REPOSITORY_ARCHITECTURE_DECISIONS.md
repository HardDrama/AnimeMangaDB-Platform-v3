# Repository Architecture Decisions

## ADR-001 — Inject Sessions

**Decision:** Repositories receive an active SQLAlchemy Session.

**Reason:** Session creation is an application concern. Injection
keeps repositories deterministic, testable, and usable within one
transaction spanning multiple repositories.

## ADR-002 — Callers Own Transactions

**Decision:** Repositories never commit or roll back.

**Reason:** A use case may require several repository operations to
succeed atomically. A repository cannot know whether its individual
operation completes the entire business transaction.

## ADR-003 — Repositories Compose Object Graphs

**Decision:** Concrete repositories resolve relationships and supply
those objects to shallow mappers.

**Reason:** Recursive mappers obscure query behavior and can create
cycles such as Series → AnimeTitle → Series.

## ADR-004 — Persistence Identity Stays Internal

**Decision:** Database primary keys are available only inside the
infrastructure layer.

**Reason:** Domain identity is represented by canonical business
values such as slugs and installment identifiers. Database IDs are
storage implementation details.

## ADR-005 — No Generic Public CRUD API

**Decision:** The base repository exposes only protected mechanics.

**Reason:** Public repository methods must express real domain
operations. A generic `update(entity)` or `find(filters)` interface
would hide semantics and create hypothetical capabilities.

## ADR-006 — Installment Identifiers Remain Strings

**Decision:** Repository queries compare persisted string
identifiers without numeric coercion.

**Reason:** Valid identifiers can include fractional values, prefixes,
suffixes, specials, and named installments.

## ADR-007 — SQLAlchemy Does Not Cross the Repository Boundary

**Decision:** Concrete repositories return Domain entities to their
consumers.

**Reason:** The API and application layers must remain independent of
SQLAlchemy state, lazy loading, Sessions, and persistence models.
