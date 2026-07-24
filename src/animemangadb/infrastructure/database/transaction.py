"""
SQLAlchemy implementation of the application transaction boundary.
"""

from __future__ import annotations

from sqlalchemy.orm import Session


class SQLAlchemyTransaction:
    """
    Commit or roll back work staged in an injected SQLAlchemy session.

    Repositories participating in one application operation must receive
    the same session instance as this transaction boundary.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the transaction boundary with a caller-owned session.
        """
        self._session = session

    def commit(self) -> None:
        """
        Permanently save all work staged in the injected session.
        """
        self._session.commit()

    def rollback(self) -> None:
        """
        Discard all uncommitted work staged in the injected session.
        """
        self._session.rollback()