# v0.6.7 Application Service Certification Validation

## Feature Checkpoint

**Version:** v0.6.7  
**Feature:** Application Service Certification  
**Status:** Certified  
**Certification Date:** July 24, 2026

## Objective

Certify the existing application-service foundation through executable
architectural gates and complete regression validation.

The checkpoint verifies that current query services depend on application
repository protocols, remain read-only, and stay independent of SQLAlchemy,
sessions, transactions, infrastructure, API, and ingestion concerns.

`TransactionProtocol` remains publicly available for future mutation-oriented
application services. No command workflow currently exists, so this checkpoint
does not claim command-service commit or rollback behavior.

## Implementation Summary

Created:

```text
tests/unit/services/test_application_service_certification.py
```

The certification test adds six executable gates:

- All six expected query services are present.
- Each query service depends on its corresponding repository protocol.
- Query services expose no mutation operations.
- Query services do not control sessions or transactions.
- `TransactionProtocol` remains available for future command services.
- The application-service layer has no forbidden infrastructure or transport
  dependencies.

Repository hygiene was also corrected by:

- Adding repository ignore rules for Python caches, test and lint caches,
  virtual environments, local environment files, build artifacts, and local
  databases.
- Removing the committed `.venv` directory from Git tracking.
- Removing committed `__pycache__` directories and Python bytecode from Git
  tracking.
- Confirming regenerated local development artifacts remain ignored.

## Certified Query-Service Dependencies

| Query service | Repository protocol |
| --- | --- |
| `SeriesQueryService` | `SeriesRepositoryProtocol` |
| `AnimeTitleQueryService` | `AnimeTitleRepositoryProtocol` |
| `MangaTitleQueryService` | `MangaTitleRepositoryProtocol` |
| `EpisodeQueryService` | `EpisodeRepositoryProtocol` |
| `ChapterQueryService` | `ChapterRepositoryProtocol` |
| `MappingQueryService` | `EpisodeChapterMappingRepositoryProtocol` |

## Files Created

```text
tests/unit/services/test_application_service_certification.py
docs/validation/V0_6_7_APPLICATION_SERVICE_CERTIFICATION_VALIDATION.md
```

## Files Updated

```text
.gitignore
ROADMAP.md
```

## Repository-Hygiene Cleanup

Previously tracked development artifacts were removed from Git tracking:

```text
.venv/
**/__pycache__/**
*.pyc
*.pyo
*.pyd
```

No production source or test-source files were removed. The local virtual
environment and regenerated caches may remain on the development machine, but
the repository now ignores them.

## Validation Commands and Results

Application-Service Certification Gates:

```bash
python -m pytest tests/unit/services/test_application_service_certification.py -q
```

Result: 6 passed

Foundation and Certification Gates:

```bash
python -m pytest tests/unit/services/test_application_services_foundation.py tests/unit/services/test_application_service_certification.py -q
```

Result: 11 passed

Repository-Protocol Tests:

```bash
python -m pytest tests/unit/services/test_series_repository_protocol.py tests/unit/services/test_title_repository_protocols.py tests/unit/services/test_installment_repository_protocols.py tests/unit/services/test_mapping_repository_protocol.py tests/unit/services/test_transaction_protocol.py -q
```

Result: 10 passed

Query-Service Behavior Tests:

```bash
python -m pytest tests/unit/services/test_series_query_service.py tests/unit/services/test_anime_title_query_service.py tests/unit/services/test_manga_title_query_service.py tests/unit/services/test_episode_query_service.py tests/unit/services/test_chapter_query_service.py tests/unit/services/test_mapping_query_service.py -q
```

Result: 23 passed

Service Test Suite:

```bash
python -m pytest tests/unit/services -q
```

Result: 44 passed

Database Infrastructure Test Suite:

```bash
python -m pytest tests/unit/infrastructure/database -q
```

Result: 194 passed

Infrastructure Test Suite:

```bash
python -m pytest tests/unit/infrastructure -q
```

Result: 194 passed

Unit Test Suite:

```bash
python -m pytest tests/unit -q
```

Result: 324 passed

Complete Project Test Suite:

```bash
python -m pytest -q
```

Result: 324 passed

Ruff:

```bash
python -m ruff check src tests
```

Result: All checks passed!

Transaction Protocol:

```bash
python -m pytest tests/unit/services/test_transaction_protocol.py -q
```

Result: 2 passed

Service-Layer SQLAlchemy Boundary:

```bash
git grep -n "sqlalchemy" -- src/animemangadb/services
```

Result: No output

Service-Layer Infrastructure Boundary:

```bash
git grep -n "animemangadb.infrastructure" -- src/animemangadb/services
```

Result: No output

Query Transaction Dependency:

```bash
git grep -n "TransactionProtocol" -- src/animemangadb/services/queries
```

Result: No output

Query Persistence Calls:

```bash
git grep -n -E "\.commit\(\)|\.rollback\(\)|\.flush\(\)" -- src/animemangadb/services/queries
```

Result: No output

Tracked Virtual Environment:

```cmd
git ls-files -- .venv
```

Result: No output

Tracked Python Cache Directories:

```cmd
git ls-files | findstr /i "__pycache__"
```

Result: No output

Tracked Python Bytecode:

```cmd
git ls-files | findstr /r /i "\.pyc$"
```

Result: No output

## Certification Gates

- Six application-service certification gates passed.
- Original application-service foundation gates remain valid.
- All expected query services are present.
- Every query service depends on its corresponding repository protocol.
- Query-service behavior tests passed.
- Query services expose no mutation operations.
- Query services contain no transaction or session control.
- Query services remain independent of SQLAlchemy and infrastructure.
- The complete application-service layer remains independent of forbidden
  infrastructure and transport dependencies.
- `TransactionProtocol` remains public and passes its tests.
- No command service currently exists.
- Service regression suite passed.
- Database regression suite passed.
- Infrastructure regression suite passed.
- Unit regression suite passed.
- Complete project regression suite passed.
- Ruff passed.
- Tracked virtual-environment and Python cache artifacts were removed.
- Generated development artifacts remain ignored.
- Documentation reviewed.
- Roadmap updated.

## Certification

The Application Service Certification checkpoint is certified for v0.6.7.

AnimeMangaDB now has executable architectural gates proving that its current
query services are protocol-driven, read-only, and independent of concrete
persistence and transport concerns.

`TransactionProtocol` remains ready for a future mutation-oriented application
workflow. That future workflow must separately certify successful commits and
failure rollbacks when it is implemented.

### Status: Certified
