# AnimeMangaDB Persistence Strategy

## Status

Accepted for Platform v3 Database Layer development.

Initial version: v0.5.1

## 1. Purpose

This document defines how AnimeMangaDB will persist its Platform v3
domain model.

The Database Layer exists to store and retrieve domain information. It
does not define domain behavior and must not become the source of truth
for business rules.

## 2. Architectural Direction

Dependencies must point inward toward the Domain Layer.

```text
Application / Infrastructure
              │
              ▼
            Domain
```

The Domain Layer must remain independent of:

- SQLAlchemy
- database engines
- database sessions
- migration frameworks
- repository implementations
- ORM persistence models

Infrastructure code may import and construct domain objects.

Domain code must never import Infrastructure code.

## 3. Domain and Persistence Models

Domain entities and ORM persistence models will be separate classes.

Domain entities model business meaning and enforce domain invariants.

ORM models represent relational storage structures and framework
requirements.

The project will not decorate domain entities as SQLAlchemy models.

The project will not add database columns, foreign keys, relationships,
or session behavior directly to domain entities.

## 4. Conversion Boundary

Dedicated mapper functions or mapper classes will convert between:

```text
Domain Entity ↔ ORM Model
```

Conversion logic will not be placed inside:

- domain entities
- API schemas
- route handlers
- SQLAlchemy model constructors
- frontend code

Mapping behavior will be implemented and tested as an explicit database
infrastructure responsibility.

## 5. Repository Boundary

Repository interfaces will operate in terms of domain objects and
domain-oriented inputs.

Repository implementations may use SQLAlchemy internally, but callers
must not be required to understand:

- SQLAlchemy sessions
- ORM query objects
- database rows
- persistence model classes

Repositories will return domain entities rather than ORM models.

Repository implementation details will remain inside the Infrastructure
Layer.

## 6. Session and Transaction Boundaries

Database sessions will be created and managed by database
infrastructure.

Domain entities will never hold database sessions.

Session ownership must be explicit. Repository methods will not create
untracked global sessions.

Transaction behavior will be introduced deliberately after the session
foundation exists.

The initial implementation will avoid hidden commits inside unrelated
domain behavior.

## 7. Initial Database Technology

The initial Platform v3 persistence implementation will use:

- SQLAlchemy 2.x
- SQLite for local development and automated validation

Database configuration must allow the connection URL to be replaced
without changing domain code.

SQLite is the initial development database, not a permanent domain
assumption.

## 8. Table Naming

Database table names will use lowercase plural snake_case names.

Planned table names:

```text
series
anime_titles
manga_titles
episodes
chapters
episode_chapter_mappings
```

Python ORM class names will use PascalCase and include an `ORM` suffix
when needed to distinguish them clearly from domain entities.

Examples:

```text
SeriesORM
AnimeTitleORM
MangaTitleORM
EpisodeORM
ChapterORM
EpisodeChapterMappingORM
```

## 9. Persistence Identity

ORM records will initially use database-generated integer primary keys.

These persistence identifiers are infrastructure concerns.

Database-generated primary keys will not automatically be added to the
current domain entities.

A separate domain identity strategy may be introduced later if domain
behavior demonstrates that explicit entity identifiers are required.

## 10. Domain Value Storage

Domain value objects will be stored using primitive database column
types.

Initial storage rules:

```text
CanonicalTitle          → string
Slug                    → string
InstallmentIdentifier   → string
```

InstallmentIdentifier must remain a string in persistence.

It must not be stored as an integer because valid identifiers include:

```text
1
10.5
SP1
```

## 11. Ownership Relationships

The relational model will preserve the domain ownership hierarchy:

```text
Series
├── AnimeTitle
│   └── Episode
└── MangaTitle
    └── Chapter
```

Planned foreign-key direction:

```text
anime_titles.series_id       → series.id
manga_titles.series_id       → series.id
episodes.anime_title_id      → anime_titles.id
chapters.manga_title_id      → manga_titles.id
```

EpisodeChapterMapping will reference exactly one Episode and one Chapter:

```text
episode_chapter_mappings.episode_id → episodes.id
episode_chapter_mappings.chapter_id → chapters.id
```

## 12. Mapping Relationships

Episode–Chapter adaptation relationships will be stored as explicit
mapping records.

The persistence model must support:

- one Episode participating in multiple mappings
- one Chapter participating in multiple mappings
- each mapping referencing exactly one Episode
- each mapping referencing exactly one Chapter

The database should prevent duplicate Episode–Chapter pairs through a
composite uniqueness constraint when ORM models are introduced.

The uniqueness rule applies to the pair:

```text
episode_id + chapter_id
```

## 13. Initial Uniqueness Strategy

The following scoped uniqueness rules are planned:

```text
Series slug
AnimeTitle slug within its Series
MangaTitle slug within its Series
Episode identifier within its AnimeTitle
Chapter identifier within its MangaTitle
Episode–Chapter mapping pair
```

These constraints will be confirmed during ORM model implementation
before being certified.

Titles alone will not be assumed globally unique.

Installment identifiers alone will not be assumed globally unique.

## 14. Deletion and Cascade Strategy

Deletion and cascade behavior will not be guessed during the foundation
checkpoint.

Cascade rules will be selected when ORM relationships are implemented
and tested.

Until then, no automatic destructive behavior is considered certified.

## 15. Migration Strategy

Schema migration tooling will be evaluated after the initial SQLAlchemy
model and metadata foundation exists.

The project will not introduce a migration framework before there is an
actual schema to migrate.

Once selected, migrations must be reproducible and committed to source
control.

## 16. Testing Strategy

Database tests will use isolated temporary databases.

Tests must not depend on a developer's persistent local database file.

Database validation will eventually include:

- metadata creation
- foreign-key behavior
- uniqueness constraints
- mapper round trips
- repository behavior
- transaction behavior
- infrastructure independence of the Domain Layer

## 17. Prohibited Designs

The following designs are not permitted unless superseded by a later
architectural decision:

- SQLAlchemy imports inside the Domain Layer
- ORM decorators on domain entities
- database sessions stored on domain entities
- API schemas used as persistence models
- ORM models returned as domain results
- integer-only installment identifier storage
- recursive Episode or Chapter ownership of mapping collections
- frontend access directly to the database
- business rules implemented only through database behavior

## 18. Planned Database Checkpoints

```text
v0.5.1 Persistence Strategy and Package Foundation
v0.5.2 SQLAlchemy Engine and Session Foundation
v0.5.3 ORM Persistence Models
v0.5.4 Domain ↔ ORM Mapping
v0.5.5 Repository Implementations
v0.5.6 Database Layer Certification
```

Checkpoint numbering may be refined as implementation evidence becomes
available.

## 19. Certification Requirement

The Database Layer may be certified only when:

- the Domain Layer remains framework independent
- the schema preserves domain ownership
- adaptation mappings support many-to-many participation
- installment identifiers remain string-compatible
- domain-to-ORM conversion is tested
- repository behavior returns domain objects
- database tests run in isolation
- the complete project test suite passes