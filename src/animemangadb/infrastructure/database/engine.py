"""
SQLAlchemy engine creation.

This module is responsible only for constructing the SQLAlchemy Engine.
"""

from __future__ import annotations

from sqlalchemy import Engine, create_engine

from .config import load_database_config


def create_database_engine() -> Engine:
    """
    Create the SQLAlchemy Engine using the configured database URL.

    The engine is created lazily. Calling this function does not create
    any tables or establish a persistent database connection.
    """

    config = load_database_config()

    return create_engine(
        config.database_url,
        future=True,
    )