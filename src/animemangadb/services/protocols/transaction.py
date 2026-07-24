"""
Application-controlled transaction protocol.
"""

from __future__ import annotations

from typing import Protocol


class TransactionProtocol(Protocol):
    """
    Transaction boundary consumed by application services.

    Implementations commit or roll back all persistence work staged
    during one application operation without exposing infrastructure
    details to the service layer.
    """

    def commit(self) -> None:
        """
        Permanently save all work staged in the transaction.
        """

    def rollback(self) -> None:
        """
        Discard all work staged in the transaction.
        """