# v0.6.5 Mapping Query Services Validation

## Feature Checkpoint

**Version:** v0.6.5  
**Feature:** Episode–Chapter Mapping Query Services  
**Status:** Certified  
**Certification Date:** July 23, 2026

## Objective

Establish the application-layer query boundary for Episode–Chapter mappings.

The feature provides read-only query services for:

- Retrieving one exact Episode–Chapter mapping.
- Listing every mapping associated with an Episode.
- Listing every mapping associated with a Chapter.
- Returning explicit missing and empty-result states.
- Keeping application services independent of the concrete database repository.

## Implementation Summary

### Repository Protocol

Created:

```text
src/animemangadb/services/protocols/episode_chapter_mapping_repository.py
```

The protocol declares the repository operations consumed by the mapping
query service:

```bash
get(episode, chapter)
exists(episode, chapter)
list_for_episode(episode)
list_for_chapter(chapter)
```

The protocol is publicly exported through:

```bash
src/animemangadb/services/protocols/__init__.py
```

### Mapping Query Service

Created:

```bash
src/animemangadb/services/queries/mapping_queries.py
```

The service provides:

```bash
get(episode, chapter) -> EpisodeChapterMapping | None
list_for_episode(episode) -> list[EpisodeChapterMapping]
list_for_chapter(chapter) -> list[EpisodeChapterMapping]
```

The service is publicly exported through:

```text
src/animemangadb/services/queries/__init__.py
```

### Application Boundary

EpisodeChapterMappingQueryService depends on
EpisodeChapterMappingRepositoryProtocol.

It does not depend directly on:

SQLAlchemy
Database sessions
ORM models
The concrete mapping repository

Database access remains inside the infrastructure repository.

### Result Semantics

Exact lookup uses:

```bash
EpisodeChapterMapping | None
```

A missing exact mapping returns:

```bash
None
```

Collection queries use:

```bash
list[EpisodeChapterMapping]
```

A query without matching mappings returns:

```bash
[]
```

## Files Created

```text
src/animemangadb/services/protocols/episode_chapter_mapping_repository.py
src/animemangadb/services/queries/mapping_queries.py
tests/unit/services/test_mapping_repository_protocol.py
tests/unit/services/test_mapping_query_service.py
```

### Files Updated

```
src/animemangadb/services/protocols/__init__.py
src/animemangadb/services/queries/__init__.py
```

## Test Coverage

The v0.6.5 tests verify:

- The concrete mapping repository exposes the required query methods.
- The application protocol declares the required query methods.
- The query service accepts its repository dependency.
- Exact lookup delegates to the repository.
- Exact lookup returns an existing mapping unchanged.
- Exact lookup returns None when a mapping is missing.
- Episode-based listing delegates to the repository.
- Episode-based listing returns mappings unchanged.
- Episode-based listing returns an empty list when no mappings exist.
- Chapter-based listing delegates to the repository.
- Chapter-based listing returns mappings unchanged.
- Chapter-based listing returns an empty list when no mappings exist.
- The protocol and service are available through their public package exports.

## Validation Commands and Results

### Focused Mapping Tests

```bash
python -m pytest tests/unit/services/test_mapping_repository_protocol.py tests/unit/services/test_mapping_query_service.py -q
```

Result: 9 passed

### Service Test Suite

```bash
python -m pytest tests/unit/services -q
```

Result: 36 passed

### Unit Test Suite

```bash
python -m pytest tests/unit -q
```

Result: 310 passed

### Ruff

```bash
python -m ruff check src tests
```

Result: All checks passed!

## Certification Gates

- Repository protocol implemented
- Concrete repository contract verified
- Exact mapping lookup implemented
- Missing exact mapping behavior verified
- Episode-based mapping query implemented
- Empty episode result behavior verified
- Chapter-based mapping query implemented
- Empty chapter result behavior verified
- Public protocol export verified
- Public query-service export verified
- Application and infrastructure boundaries preserved
- Focused tests passed
- Service regression suite passed
- Unit regression suite passed
- Complete project regression suite passed
- Ruff passed
- Documentation reviewed

## Certification

Episode–Chapter Mapping Query Services are certified for v0.6.5.

The application layer now exposes a complete read-only query boundary for
exact, Episode-based, and Chapter-based mapping retrieval while preserving
the separation between application services and database infrastructure.

### Status: Certified