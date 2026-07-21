from animemangadb.domain.exceptions import ValidationError
from animemangadb.domain.value_objects.installment_identifier import (
    InstallmentIdentifier,
)

import pytest


def test_valid_numeric_identifier():
    identifier = InstallmentIdentifier("1")

    assert identifier.value == "1"


def test_valid_decimal_identifier():
    identifier = InstallmentIdentifier("12.5")

    assert identifier.value == "12.5"


def test_valid_special_identifier():
    identifier = InstallmentIdentifier("SP1")

    assert identifier.value == "SP1"


def test_identifier_is_trimmed():
    identifier = InstallmentIdentifier("  EX  ")

    assert identifier.value == "EX"


def test_empty_identifier_raises_validation_error():
    with pytest.raises(ValidationError):
        InstallmentIdentifier("")


def test_whitespace_identifier_raises_validation_error():
    with pytest.raises(ValidationError):
        InstallmentIdentifier("     ")


def test_none_identifier_raises_validation_error():
    with pytest.raises(ValidationError):
        InstallmentIdentifier(None)  # type: ignore[arg-type]


def test_identifier_equality():
    assert (
        InstallmentIdentifier("12")
        == InstallmentIdentifier("12")
    )


def test_identifier_hashable():
    identifiers = {
        InstallmentIdentifier("1"),
        InstallmentIdentifier("2"),
    }

    assert InstallmentIdentifier("1") in identifiers


def test_string_representation():
    identifier = InstallmentIdentifier("OVA-2")

    assert str(identifier) == "OVA-2"