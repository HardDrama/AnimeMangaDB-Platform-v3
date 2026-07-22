"""Tests for Series, AnimeTitle, and MangaTitle mappers."""

import pytest
from sqlalchemy import inspect as sqlalchemy_inspect

from animemangadb.domain.entities import (
    AnimeTitle,
    MangaTitle,
    Series,
)
from animemangadb.domain.exceptions import ValidationError
from animemangadb.domain.value_objects.canonical_title import (
    CanonicalTitle,
)
from animemangadb.infrastructure.database.mappers import (
    AnimeTitleMapper,
    MangaTitleMapper,
    Mapper,
    SeriesMapper,
)
from animemangadb.infrastructure.database.models import (
    AnimeTitleORM,
    MangaTitleORM,
    SeriesORM,
)


def make_series() -> Series:
    return Series(
        title=CanonicalTitle("One Piece"),
    )


def test_title_mappers_inherit_from_mapper():
    assert issubclass(SeriesMapper, Mapper)
    assert issubclass(AnimeTitleMapper, Mapper)
    assert issubclass(MangaTitleMapper, Mapper)


def test_series_to_orm_maps_scalar_fields():
    domain_object = make_series()

    orm_object = SeriesMapper.to_orm(domain_object)

    assert isinstance(orm_object, SeriesORM)
    assert orm_object.title == "One Piece"
    assert orm_object.slug == "one-piece"
    assert "id" not in orm_object.__dict__


def test_series_to_orm_creates_new_unattached_objects():
    domain_object = make_series()

    first = SeriesMapper.to_orm(domain_object)
    second = SeriesMapper.to_orm(domain_object)

    assert first is not second
    assert sqlalchemy_inspect(first).session is None
    assert sqlalchemy_inspect(second).session is None


def test_series_to_domain_reconstructs_value_objects():
    orm_object = SeriesORM(
        title="One Piece",
        slug="one-piece",
    )

    domain_object = SeriesMapper.to_domain(orm_object)

    assert isinstance(domain_object, Series)
    assert isinstance(
        domain_object.title,
        CanonicalTitle,
    )
    assert domain_object.title.value == "One Piece"
    assert domain_object.slug.value == "one-piece"


def test_series_round_trip_preserves_domain_state():
    original = make_series()

    restored = SeriesMapper.to_domain(
        SeriesMapper.to_orm(original)
    )

    assert restored is not original
    assert restored.title == original.title
    assert restored.slug == original.slug


def test_series_to_domain_rejects_inconsistent_slug():
    orm_object = SeriesORM(
        title="One Piece",
        slug="incorrect-slug",
    )

    with pytest.raises(ValidationError):
        SeriesMapper.to_domain(orm_object)


def test_anime_title_to_orm_uses_resolved_parent():
    series = make_series()
    series_orm = SeriesMapper.to_orm(series)
    domain_object = AnimeTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )

    orm_object = AnimeTitleMapper.to_orm(
        domain_object,
        series_orm=series_orm,
    )

    assert isinstance(orm_object, AnimeTitleORM)
    assert orm_object.series is series_orm
    assert orm_object.title == "One Piece"
    assert orm_object.slug == "one-piece"
    assert orm_object.episodes == []


def test_anime_title_to_domain_uses_resolved_parent():
    series = make_series()
    orm_object = AnimeTitleORM(
        title="One Piece",
        slug="one-piece",
    )

    domain_object = AnimeTitleMapper.to_domain(
        orm_object,
        series=series,
    )

    assert isinstance(domain_object, AnimeTitle)
    assert domain_object.series is series
    assert domain_object.title.value == "One Piece"
    assert domain_object.slug.value == "one-piece"


def test_anime_title_round_trip_preserves_state():
    series = make_series()
    series_orm = SeriesMapper.to_orm(series)
    original = AnimeTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )

    restored = AnimeTitleMapper.to_domain(
        AnimeTitleMapper.to_orm(
            original,
            series_orm=series_orm,
        ),
        series=series,
    )

    assert restored is not original
    assert restored.series is series
    assert restored.title == original.title
    assert restored.slug == original.slug


def test_anime_title_to_domain_rejects_inconsistent_slug():
    series = make_series()
    orm_object = AnimeTitleORM(
        title="One Piece",
        slug="incorrect-slug",
    )

    with pytest.raises(ValidationError):
        AnimeTitleMapper.to_domain(
            orm_object,
            series=series,
        )


def test_manga_title_to_orm_uses_resolved_parent():
    series = make_series()
    series_orm = SeriesMapper.to_orm(series)
    domain_object = MangaTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )

    orm_object = MangaTitleMapper.to_orm(
        domain_object,
        series_orm=series_orm,
    )

    assert isinstance(orm_object, MangaTitleORM)
    assert orm_object.series is series_orm
    assert orm_object.title == "One Piece"
    assert orm_object.slug == "one-piece"
    assert orm_object.chapters == []


def test_manga_title_to_domain_uses_resolved_parent():
    series = make_series()
    orm_object = MangaTitleORM(
        title="One Piece",
        slug="one-piece",
    )

    domain_object = MangaTitleMapper.to_domain(
        orm_object,
        series=series,
    )

    assert isinstance(domain_object, MangaTitle)
    assert domain_object.series is series
    assert domain_object.title.value == "One Piece"
    assert domain_object.slug.value == "one-piece"


def test_manga_title_round_trip_preserves_state():
    series = make_series()
    series_orm = SeriesMapper.to_orm(series)
    original = MangaTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )

    restored = MangaTitleMapper.to_domain(
        MangaTitleMapper.to_orm(
            original,
            series_orm=series_orm,
        ),
        series=series,
    )

    assert restored is not original
    assert restored.series is series
    assert restored.title == original.title
    assert restored.slug == original.slug


def test_manga_title_to_domain_rejects_inconsistent_slug():
    series = make_series()
    orm_object = MangaTitleORM(
        title="One Piece",
        slug="incorrect-slug",
    )

    with pytest.raises(ValidationError):
        MangaTitleMapper.to_domain(
            orm_object,
            series=series,
        )


def test_mapper_inputs_are_not_mutated():
    series = make_series()
    original_title = series.title
    original_slug = series.slug

    SeriesMapper.to_orm(series)

    assert series.title is original_title
    assert series.slug is original_slug


def test_title_mapper_methods_reject_wrong_types():
    with pytest.raises(TypeError):
        SeriesMapper.to_orm("One Piece")

    with pytest.raises(TypeError):
        SeriesMapper.to_domain("One Piece")
