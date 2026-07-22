# Domain ↔ ORM Mapping Strategy

## Purpose

This document defines how AnimeMangaDB converts between certified Domain
entities and SQLAlchemy ORM persistence models.

The strategy prevents recursive graph conversion, duplicate object
construction, accidental persistence coupling, and SQLAlchemy state from
leaking into the Domain Layer.

## Dependency Direction

```text
Infrastructure → Domain
Domain ✕ Infrastructure
```

Database mappers may import Domain entities and ORM models.

Domain modules must never import database mappers, SQLAlchemy, ORM models,
repositories, sessions, or engines.

## Core Decision: Shallow Entity Mappers

Every concrete entity mapper performs shallow conversion.

A shallow mapper converts only the scalar state directly owned by the source
object. It does not recursively convert parent relationships, child
collections, or many-to-many relationships.

Examples:

```text
SeriesMapper
maps: title, slug
ignores: anime_titles, manga_titles

AnimeTitleMapper
maps: title, slug
ignores: series, episodes

EpisodeMapper
maps: identifier, title, slug
ignores: anime_title, chapter_mappings
```

## Object-Graph Ownership

Repositories own object-graph composition.

Repositories are responsible for:

- querying related ORM rows;
- selecting which relationships are required;
- invoking shallow mappers;
- connecting mapped Domain objects;
- assigning ORM foreign keys and relationships during persistence;
- preventing duplicate objects within one repository operation.

Mappers are not responsible for database queries or relationship loading.

## Recursion Rule

A mapper must never recursively invoke a mapper for a parent, child collection,
or bidirectional relationship.

This prevents cycles such as:

```text
Series → AnimeTitle → Series
Episode → EpisodeChapterMapping → Episode
Chapter → EpisodeChapterMapping → Chapter
```

## Persistence Identity

SQLAlchemy primary keys are persistence identity.

Persistence identity is not copied into a Domain entity unless that entity
explicitly defines a matching Domain concept.

Current Domain entities do not gain database IDs merely because ORM models
contain integer primary keys.

## Domain → ORM Conversion

A `to_orm()` conversion:

- creates a new ORM object;
- maps scalar Domain values;
- does not query the database;
- does not attach the object to a Session;
- does not assign parent relationships automatically;
- does not populate child collections automatically;
- does not copy a database primary key from unrelated state.

Repositories assign foreign keys and relationships after resolving the required
persisted objects.

## ORM → Domain Conversion

A `to_domain()` conversion:

- creates a new Domain object;
- maps scalar ORM values;
- does not trigger relationship traversal intentionally;
- does not expose SQLAlchemy instrumentation;
- does not preserve Session attachment;
- does not copy persistence-only identity into the Domain.

Repositories compose aggregate graphs from the resulting shallow Domain
objects.

## Installment Identifiers

Episode and Chapter identifiers remain strings in both directions.

Mappers must not coerce identifiers to integers or floating-point numbers.

Valid examples include:

```text
1
10.5
SP1
```

## Episode–Chapter Mapping

`EpisodeChapterMappingMapper` is coordinated by a repository.

The repository first resolves or maps the participating Episode and Chapter
objects. The mapper then constructs the mapping from those already-resolved
objects.

The mapping mapper must not recursively reload or remap full Episode and
Chapter graphs.

## Default Mapping Policy

The code-level default policy is:

```text
map_scalar_fields = true
map_relationships = false
preserve_persistence_identity = false
repository_composes_object_graphs = true
```

This policy is immutable and shared by all concrete mappers.

## Prohibited Designs

The following designs are prohibited:

- recursive bidirectional graph mapping;
- database queries inside mappers;
- Session creation inside mappers;
- ORM objects returned outside Infrastructure repositories;
- SQLAlchemy imports inside the Domain Layer;
- copying ORM primary keys into Domain entities without a Domain rule;
- automatic relationship traversal during shallow conversion;
- identifier conversion from string to numeric types.

## Testing Requirements

Concrete mapper tests must verify:

- Domain → ORM scalar conversion;
- ORM → Domain scalar conversion;
- new-object creation;
- no mutation of input objects;
- string identifier preservation;
- ignored relationship collections;
- no database queries;
- compliance with the default mapping policy.

Repository tests will separately verify graph composition and persistence
relationships.

## Certification Boundary

This strategy checkpoint defines and tests mapping rules.

It intentionally does not introduce:

- concrete entity mappers;
- repositories;
- database queries;
- persistence operations;
- aggregate loading behavior.
