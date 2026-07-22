from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from animemangadb.infrastructure.database import Base


def test_base_is_declarative_base():
    assert issubclass(
        Base,
        DeclarativeBase,
    )


def test_base_has_metadata():
    assert isinstance(
        Base.metadata,
        MetaData,
    )


def test_metadata_has_table_collection():
    assert hasattr(
        Base.metadata,
        "tables",
    )


def test_metadata_object_is_shared():
    first = Base.metadata
    second = Base.metadata

    assert first is second


def test_base_can_be_imported():
    assert Base is not None


def test_metadata_schema_is_none():
    assert Base.metadata.schema is None


def test_metadata_is_mutable_by_sqlalchemy():
    metadata = Base.metadata

    assert hasattr(
        metadata,
        "tables",
    )