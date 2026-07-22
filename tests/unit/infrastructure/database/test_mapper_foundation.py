from abc import ABC

import pytest

from animemangadb.infrastructure.database.mappers import (
    Mapper,
)


def test_mapper_is_abstract():
    assert issubclass(
        Mapper,
        ABC,
    )


def test_mapper_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Mapper()


def test_mapper_declares_to_domain():
    assert hasattr(
        Mapper,
        "to_domain",
    )


def test_mapper_declares_to_orm():
    assert hasattr(
        Mapper,
        "to_orm",
    )


def test_mapper_methods_are_static():
    mapper_dict = Mapper.__dict__

    assert isinstance(
        mapper_dict["to_domain"],
        staticmethod,
    )
    assert isinstance(
        mapper_dict["to_orm"],
        staticmethod,
    )


def test_mapper_has_type_parameters():
    assert (
        len(Mapper.__parameters__)
        == 2
    )


def test_mapper_exports_are_correct():
    from animemangadb.infrastructure.database.mappers import (
        Mapper as ImportedMapper,
    )

    assert ImportedMapper is Mapper


def test_mapper_has_expected_method_names():
    assert Mapper.to_domain.__name__ == "to_domain"
    assert Mapper.to_orm.__name__ == "to_orm"