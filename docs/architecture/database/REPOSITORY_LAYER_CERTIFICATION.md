# Repository Layer Certification

v0.5.9 establishes the SQLAlchemy repository layer as the sole persistence-facing composition boundary for Domain entities.

## Certified decisions
- Callers create Sessions and own commit, rollback, and close.
- Repositories may stage, query, flush, refresh, and delete.
- Repositories compose Domain object graphs from shallow mappers.
- Mappers do not query or recurse.
- ORM objects and persistence IDs remain internal to infrastructure.
- Series/title slugs and installment identifiers form business-facing lookup scopes.
- Installment identifiers remain strings.
- The repository package exposes one concrete repository for every current Domain entity.

## Certified flow
Domain → Repository → Mapper → ORM → SQLAlchemy Session → Database

The reverse read path reconstructs Domain graphs while preventing SQLAlchemy objects and persistence identity from crossing the infrastructure boundary.
