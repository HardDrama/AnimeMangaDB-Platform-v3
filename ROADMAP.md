# AnimeMangaDB Platform v3 Roadmap

## Completed

### v0.1.0 — Platform Foundation

- Repository and package structure
- Python environment
- Dependency management
- Pytest and Ruff foundation
- Initial smoke validation

### v0.2.0 — Architecture Documentation

- Series-first platform architecture
- Layer responsibilities
- Dependency rules
- Backend and frontend boundaries

### v0.3.0 — Domain Specification

- Authoritative domain specification
- Series aggregate definition
- Anime and manga sibling branches
- Episode and chapter ownership rules
- Explicit adaptation mapping model
- Identity and validation rules
- Domain invariants
- Future expansion policy
- Initial Architecture Decision Records

### v0.4.0 — Domain Layer

- Domain identifiers
- Local installment identity value object
- Series entity
- Anime Title entity
- Episode entity
- Manga Title entity
- Chapter entity
- Episode-Chapter Mapping entity
- Domain exceptions
- Domain unit tests

### v0.5.0 — Database Layer

### v0.6.0 — Repository Layer
• v0.6.0 Application Services Foundation
• v0.6.1 Repository Protocol Foundation 
• v0.6.2 Series Query Service 
• v0.6.3 Title Query Services 
• v0.6.4 Installment Query Services

### v0.6.5 — Episode–Chapter Mapping Query Services

**Status:** Certified

- [x] Define the mapping repository protocol.
- [x] Add exact Episode–Chapter mapping lookup.
- [x] Add Episode-based mapping queries.
- [x] Add Chapter-based mapping queries.
- [x] Verify missing and empty-result behavior.
- [x] Verify public service and protocol exports.
- [x] Complete regression validation.
- [x] Certify the feature checkpoint.

### v0.6.6 Transaction Boundary

- Added an application-layer transaction protocol.
- Added the SQLAlchemy transaction adapter.
- Preserved caller ownership of the injected session.
- Verified exact commit and rollback delegation.
- Verified atomic commit across multiple repositories.
- Verified atomic rollback across multiple repositories.
- Preserved the application/infrastructure dependency boundary.
- Certified with 318 passing tests and clean Ruff validation.

## Current 

### v0.6.7 Application Service Certification

- Verify application services depend on repository protocols.
- Verify application services depend on `TransactionProtocol`.
- Verify successful operations commit.
- Verify failed operations roll back.
- Verify services contain no ORM or session behavior.
- Certify the complete application-service foundation.

## Future

### v0.7.0 — Service Layer
### v0.8.0 — Ingestion Layer
### v0.9.0 — API Layer
### v0.10.0 — Frontend
### Platform Checkpoint v1