# Platform v3 Dependency Rules

## Purpose

These rules prevent Platform v3 from recreating the cyclic coupling of the legacy platform.

## Domain rules

`animemangadb.domain` may use the Python standard library. It must not import API, data, ingestion, services, tools, SQLAlchemy, FastAPI, or frontend code.

## Service rules

`animemangadb.services` may import domain types and repository interfaces. It must not define HTTP routes or contain SQLAlchemy queries.

## Data rules

`animemangadb.data` may import domain types. It owns ORM models, repositories, transactions, and migrations, but not application workflows.

## Ingestion rules

`animemangadb.ingestion` owns provider-specific crawling, extraction, parsing, and normalization. It must not write directly through ORM sessions.

## API rules

`animemangadb.api` calls application services. It must not issue database queries directly or duplicate domain validation.

## Tools rules

`animemangadb.tools` calls application services and must not bypass repositories through direct ORM writes.

## Frontend rules

The top-level `frontend` application communicates with the backend through the REST API only.

## Relationship rule

Episodes and chapters are siblings under a series.

Forbidden assumptions:

```text
Episode owns Chapter
Chapter owns Episode
Anime repository owns Manga
Manga repository owns Anime
```

Allowed model:

```text
Episode ── EpisodeChapterMapping ── Chapter
```

## Enforcement

Initially these rules are certified through documentation and package-layout tests. Static import-boundary checks will be added as implementation grows.
