"""
Transaction Protocol Tests

Feature Checkpoint
v0.6.6
"""

from animemangadb.services.protocols import (
    TransactionProtocol,
)
from animemangadb.services.protocols.transaction import (
    TransactionProtocol as DirectTransactionProtocol,
)


def test_transaction_protocol_declares_required_methods():
    required_methods = (
        "commit",
        "rollback",
    )

    for method in required_methods:
        assert hasattr(
            TransactionProtocol,
            method,
        )


def test_transaction_protocol_is_publicly_exported():
    assert TransactionProtocol is DirectTransactionProtocol