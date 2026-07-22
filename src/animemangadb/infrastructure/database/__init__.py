"""
Database infrastructure for AnimeMangaDB.

This package will contain:

- SQLAlchemy configuration
- ORM persistence models
- domain-to-persistence mappers
- repository implementations
- transaction and session management

The package intentionally contains no database implementation during
v0.5.1. This checkpoint establishes the package boundary and persistence
strategy before framework-specific behavior is introduced.
"""