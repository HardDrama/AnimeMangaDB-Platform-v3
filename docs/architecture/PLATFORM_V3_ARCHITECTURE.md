# AnimeMangaDB Platform v3 Architecture

## Purpose

Platform v3 is a domain-first rebuild of AnimeMangaDB.

The platform models a franchise or property as a `Series` with parallel anime and manga branches. Episodes and chapters belong to their own titles. Adaptation relationships are explicit mappings rather than ownership.

## Domain tree

```text
Series
├── Anime
│   ├── Anime Title
│   │   └── Episodes
│   │       └── Episode Detail
│   │           └── Adapted Chapters
│   └── Additional Anime Titles
│
└── Manga
    ├── Manga Title
    │   └── Chapters
    │       └── Chapter Detail
    │           └── Adapted Episodes
    └── Additional Manga Titles
```

Example:

```text
Naruto
├── Anime
│   ├── Naruto
│   │   └── Episodes
│   └── Naruto Shippuden
│       └── Episodes
│
└── Manga
    └── Naruto
        └── Chapters
```

A chapter may link to episodes from more than one anime title. An episode may link to one or more chapters.

## Core entities

### Series

The aggregate root representing the overall property or franchise.

### Anime title

A distinct animated production under a series.

### Episode

An episode belonging to exactly one anime title.

### Manga title

A distinct manga publication under a series.

### Chapter

A chapter belonging to exactly one manga title.

### Episode-chapter mapping

An explicit relationship between an episode and a chapter. The mapping does not give ownership of either side to the other.

## Platform layers

```text
Domain
    ↓
Application Services
    ↓
Data Access
    ↓
Database

Ingestion
    ↓
Validated Domain Input
    ↓
Application Services

REST API / CLI / Tools
    ↓
Application Services

Website
    ↓
REST API
```

### Domain

Owns entities, value objects, domain validation, terminology, and relationship rules. It remains independent of infrastructure.

### Ingestion

Owns crawling, fetching, provider adapters, extraction, parsing, normalization, and source provenance.

### Data

Owns ORM models, schema, migrations, repositories, transactions, indexes, and constraints.

### Services

Owns application use cases and orchestration across repositories.

### API

Owns routes, transport schemas, pagination, filtering, error contracts, OpenAPI documentation, and health endpoints.

### Tools

Owns administrative commands, imports, repairs, comparisons, reports, certification, migrations, and initialization.

### Frontend

The frontend is a separate top-level application. It consumes the REST API and remains thin.

## Repository layout

```text
src/animemangadb/
├── api/
├── config/
├── data/
├── domain/
├── ingestion/
├── services/
└── tools/

frontend/
docs/
tests/
scripts/
```

## Development lifecycle

```text
Build → Test → Document → Validate → Certify
```

## Platform rule

The domain drives the architecture. Database convenience, API shape, and frontend implementation must not distort the domain model.
