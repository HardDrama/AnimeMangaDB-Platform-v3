"""
SQLAlchemy session factory.
"""

from __future__ import annotations

from sqlalchemy.orm import Session, sessionmaker

from .engine import create_database_engine

_engine = create_database_engine()

SessionFactory = sessionmaker(
    bind=_engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
)