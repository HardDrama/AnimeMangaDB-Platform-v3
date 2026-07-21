# Platform v3

## Version 0.1.0

### Foundation

### Added
• Clean repository
• Modern src layout
• Domain-first package structure
• Testing framework
• Python environment
• Development dependencies
• Validation framework

### Validated
• Repository initialization
• Environment setup
• Test framework

### Status
• Certified

## v0.2.0 — Architecture Documentation

### Added

- Platform v3 architecture specification
- Series-first domain tree
- Explicit platform dependency rules
- Backend Python package boundaries
- Top-level frontend application boundary
- Package-boundary validation tests

### Established

- Series as the platform aggregate root
- Anime and manga as parallel branches
- Episode and chapter ownership boundaries
- Explicit episode-chapter mapping relationship
- Domain-first dependency direction

### Validated

- Backend `src` package layout
- Frontend separation
- Expected backend package structure
- Complete unit test suite
- Ruff lint validation

### Status

Certified

## v0.3.0 — Domain Specification

### Added

- Authoritative Platform v3 Domain Specification
- Domain terminology and entity definitions
- Aggregate and ownership rules
- Identity and validation rules
- Lifecycle rules and domain invariants
- Future expansion and change-control policy
- Four initial Architecture Decision Records
- Automated domain-document completeness tests

### Established

- Series as the aggregate root
- Anime Titles and Manga Titles as sibling branches
- Anime Title ownership of Episodes
- Manga Title ownership of Chapters
- Explicit Episode-Chapter Mapping relationships
- Same-Series mapping constraint
- Support for non-integer installment identifiers
- Specification-first domain change policy

### Validated

- Required specification sections
- Core entity definitions
- Accepted ADR structure
- Complete unit suite
- Ruff lint validation

### Status

Certified