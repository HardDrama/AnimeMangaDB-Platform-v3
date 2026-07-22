"""
Base mapper interface.

Every mapper converts between a Domain object and an ORM object.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

DomainT = TypeVar("DomainT")
OrmT = TypeVar("OrmT")


class Mapper(Generic[DomainT, OrmT], ABC):
    """
    Base class for all database mappers.
    """

    @staticmethod
    @abstractmethod
    def to_domain(
        orm_object: OrmT,
    ) -> DomainT:
        """
        Convert an ORM object into a Domain object.
        """

    @staticmethod
    @abstractmethod
    def to_orm(
        domain_object: DomainT,
    ) -> OrmT:
        """
        Convert a Domain object into an ORM object.
        """