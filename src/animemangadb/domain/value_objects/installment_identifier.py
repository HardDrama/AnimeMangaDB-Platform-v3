"""
Domain value object representing an installment identifier.
"""

from dataclasses import dataclass

from animemangadb.domain.exceptions import ValidationError

from .base import ValueObject


@dataclass(frozen=True)
class InstallmentIdentifier(ValueObject):
    """
    Immutable domain value object representing an installment identifier.

    Examples:
        1
        12
        12.5
        SP1
        OVA-2
        EX
        Special-1
    """

    value: str

    def __post_init__(self) -> None:
        """Validate and normalize the identifier."""

        if not isinstance(self.value, str):
            raise ValidationError(
                "Installment identifier must be a string."
            )

        trimmed = self.value.strip()

        if not trimmed:
            raise ValidationError(
                "Installment identifier cannot be empty."
            )

        object.__setattr__(self, "value", trimmed)

    def __str__(self) -> str:
        """Return the normalized identifier."""
        return self.value