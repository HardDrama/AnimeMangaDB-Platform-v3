"""
Application services and use-case orchestration.

This package coordinates domain operations through abstract repository
boundaries. It must not contain persistence models, SQLAlchemy behavior,
HTTP transport concerns, provider crawling, or frontend logic.
"""

from animemangadb.services.exceptions import ApplicationServiceError

__all__ = [
    "ApplicationServiceError",
]