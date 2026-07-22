"""
Shared SQLAlchemy declarative base.

All ORM persistence models will inherit from Base.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Root declarative base for all ORM models.

    This class intentionally contains no custom behavior.
    It provides a shared SQLAlchemy MetaData instance
    that will collect every ORM table definition.
    """

    pass