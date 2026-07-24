"""
Series Command Service Tests

Feature Checkpoint
v0.7.0
"""

from unittest.mock import Mock

import pytest

from animemangadb.domain.entities import Series
from animemangadb.domain.exceptions import ValidationError
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.services import SeriesAlreadyExistsError
from animemangadb.services.commands import SeriesCommandService


def test_create_persists_and_commits_series():
    repository = Mock()
    transaction = Mock()
    service = SeriesCommandService(repository, transaction)
    title = CanonicalTitle("One Piece")

    repository.exists_by_slug.return_value = False
    repository.add.side_effect = lambda series: series

    result = service.create(title)

    assert isinstance(result, Series)
    assert result.title is title
    assert result.slug.value == "one-piece"
    repository.exists_by_slug.assert_called_once_with(result.slug)
    repository.add.assert_called_once_with(result)
    transaction.commit.assert_called_once_with()
    transaction.rollback.assert_not_called()


def test_create_rejects_existing_series_and_rolls_back():
    repository = Mock()
    transaction = Mock()
    service = SeriesCommandService(repository, transaction)
    title = CanonicalTitle("One Piece")

    repository.exists_by_slug.return_value = True

    with pytest.raises(
        SeriesAlreadyExistsError,
        match="A Series with slug 'one-piece' already exists.",
    ) as error:
        service.create(title)

    assert error.value.slug.value == "one-piece"
    repository.exists_by_slug.assert_called_once_with(
        Series(title).slug,
    )
    repository.add.assert_not_called()
    transaction.commit.assert_not_called()
    transaction.rollback.assert_called_once_with()


def test_create_rolls_back_when_series_construction_fails():
    repository = Mock()
    transaction = Mock()
    service = SeriesCommandService(repository, transaction)

    with pytest.raises(
        ValidationError,
        match="Series title must be a CanonicalTitle.",
    ):
        service.create("One Piece")  # type: ignore[arg-type]

    repository.exists_by_slug.assert_not_called()
    repository.add.assert_not_called()
    transaction.commit.assert_not_called()
    transaction.rollback.assert_called_once_with()


def test_create_rolls_back_when_repository_add_fails():
    repository = Mock()
    transaction = Mock()
    service = SeriesCommandService(repository, transaction)
    error = RuntimeError("persistence failed")

    repository.exists_by_slug.return_value = False
    repository.add.side_effect = error

    with pytest.raises(RuntimeError, match="persistence failed"):
        service.create(CanonicalTitle("One Piece"))

    transaction.commit.assert_not_called()
    transaction.rollback.assert_called_once_with()


def test_create_rolls_back_when_commit_fails():
    repository = Mock()
    transaction = Mock()
    service = SeriesCommandService(repository, transaction)
    error = RuntimeError("commit failed")

    repository.exists_by_slug.return_value = False
    repository.add.side_effect = lambda series: series
    transaction.commit.side_effect = error

    with pytest.raises(RuntimeError, match="commit failed"):
        service.create(CanonicalTitle("One Piece"))

    transaction.rollback.assert_called_once_with()
