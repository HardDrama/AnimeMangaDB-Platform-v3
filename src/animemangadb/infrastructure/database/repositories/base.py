"""Shared repository foundation for SQLAlchemy-backed repositories."""

from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from animemangadb.infrastructure.database.base import Base

ORMModelT = TypeVar(
    "ORMModelT",
    bound=Base,
)


class Repository(ABC, Generic[ORMModelT]):
    """Base class for concrete SQLAlchemy repositories.

    Repositories receive an already-created Session. They may stage,
    query, flush, and refresh persistence objects, but they never
    commit or roll back the transaction. Transaction ownership stays
    with the application boundary that created the Session.
    """

    orm_model: type[ORMModelT]

    def __init__(self, session: Session) -> None:
        if session is None:
            raise TypeError(
                "session must not be None."
            )

        self._session = session

    def _add(self, orm_object: ORMModelT) -> ORMModelT:
        """Stage an ORM object in the current Session."""
        self._session.add(orm_object)
        return orm_object

    def _delete(self, orm_object: ORMModelT) -> None:
        """Stage an ORM object for deletion."""
        self._session.delete(orm_object)

    def _flush(self) -> None:
        """Flush pending persistence changes without committing."""
        self._session.flush()

    def _refresh(self, orm_object: ORMModelT) -> None:
        """Refresh an ORM object from current database state."""
        self._session.refresh(orm_object)

    def _get_by_persistence_id(
        self,
        persistence_id: int,
    ) -> ORMModelT | None:
        """Return one ORM row by its infrastructure identity."""
        if not isinstance(persistence_id, int):
            raise TypeError(
                "persistence_id must be an integer."
            )

        return self._session.get(
            self.orm_model,
            persistence_id,
        )

    def _one_or_none(
        self,
        statement: Select[tuple[ORMModelT]],
    ) -> ORMModelT | None:
        """Execute a select expected to return at most one row."""
        return self._session.scalars(
            statement
        ).one_or_none()

    def _list(
        self,
        statement: Select[tuple[ORMModelT]],
    ) -> list[ORMModelT]:
        """Execute a select and return its rows as a new list."""
        result: Sequence[ORMModelT] = (
            self._session.scalars(
                statement
            ).all()
        )
        return list(result)

    def _exists(self, *criteria: object) -> bool:
        """Return whether the repository model matches criteria."""
        statement = (
            select(self.orm_model)
            .where(*criteria)
            .limit(1)
        )
        return self._session.scalar(statement) is not None
