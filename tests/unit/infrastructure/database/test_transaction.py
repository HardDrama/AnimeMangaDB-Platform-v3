"""
SQLAlchemy Transaction Tests

Feature Checkpoint
v0.6.6
"""

from unittest.mock import Mock

from sqlalchemy.orm import Session

from animemangadb.infrastructure.database import (
    SQLAlchemyTransaction,
)
from animemangadb.services.protocols import (
    TransactionProtocol,
)


def test_sqlalchemy_transaction_uses_injected_session():
    session = Mock(spec=Session)

    transaction = SQLAlchemyTransaction(session)

    assert transaction._session is session
    session.commit.assert_not_called()
    session.rollback.assert_not_called()


def test_sqlalchemy_transaction_satisfies_transaction_protocol():
    session = Mock(spec=Session)
    transaction: TransactionProtocol = SQLAlchemyTransaction(
        session,
    )

    assert callable(transaction.commit)
    assert callable(transaction.rollback)


def test_commit_delegates_to_injected_session_once():
    session = Mock(spec=Session)
    transaction = SQLAlchemyTransaction(session)

    transaction.commit()

    session.commit.assert_called_once_with()
    session.rollback.assert_not_called()


def test_rollback_delegates_to_injected_session_once():
    session = Mock(spec=Session)
    transaction = SQLAlchemyTransaction(session)

    transaction.rollback()

    session.rollback.assert_called_once_with()
    session.commit.assert_not_called()