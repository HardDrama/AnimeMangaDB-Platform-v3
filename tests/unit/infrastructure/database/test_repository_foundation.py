"""Tests for the shared repository foundation."""

from collections.abc import Iterator

import pytest
from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import (
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)

from sqlalchemy.orm import DeclarativeBase
from animemangadb.infrastructure.database.repositories import (
    Repository,
)


class RepositoryTestBase(DeclarativeBase):
    """Private metadata for repository foundation tests."""


class RepositoryFixtureORM(RepositoryTestBase):
    __tablename__ = "repository_fixture"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )


class RepositoryFixture(
    Repository[RepositoryFixtureORM]
):
    orm_model = RepositoryFixtureORM

    def add(
        self,
        name: str,
    ) -> RepositoryFixtureORM:
        return self._add(
            RepositoryFixtureORM(name=name)
        )

    def delete(
        self,
        orm_object: RepositoryFixtureORM,
    ) -> None:
        self._delete(orm_object)

    def flush(self) -> None:
        self._flush()

    def refresh(
        self,
        orm_object: RepositoryFixtureORM,
    ) -> None:
        self._refresh(orm_object)

    def get_by_id(
        self,
        persistence_id: int,
    ) -> RepositoryFixtureORM | None:
        return self._get_by_persistence_id(
            persistence_id
        )

    def get_by_name(
        self,
        name: str,
    ) -> RepositoryFixtureORM | None:
        statement = select(
            RepositoryFixtureORM
        ).where(
            RepositoryFixtureORM.name == name
        )
        return self._one_or_none(statement)

    def list_all(
        self,
    ) -> list[RepositoryFixtureORM]:
        statement = select(
            RepositoryFixtureORM
        ).order_by(
            RepositoryFixtureORM.id
        )
        return self._list(statement)

    def exists_by_name(
        self,
        name: str,
    ) -> bool:
        return self._exists(
            RepositoryFixtureORM.name == name
        )


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:"
    )
    RepositoryTestBase.metadata.create_all(engine)
    session_factory = sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    with session_factory() as current_session:
        yield current_session

    RepositoryTestBase.metadata.drop_all(engine)
    engine.dispose()


def test_repository_requires_session():
    with pytest.raises(TypeError):
        RepositoryFixture(None)


def test_repository_stages_new_object(
    session: Session,
):
    repository = RepositoryFixture(session)

    orm_object = repository.add("One Piece")

    assert orm_object in session.new
    assert orm_object.id is None


def test_flush_assigns_identity_without_commit(
    session: Session,
):
    repository = RepositoryFixture(session)
    orm_object = repository.add("One Piece")

    repository.flush()

    assert orm_object.id is not None
    assert session.in_transaction()
    assert session.get(
        RepositoryFixtureORM,
        orm_object.id,
    ) is orm_object


def test_repository_does_not_commit_implicitly(
    session: Session,
):
    repository = RepositoryFixture(session)
    repository.add("One Piece")

    assert session.new
    assert session.in_transaction()

    session.rollback()

    assert repository.list_all() == []


def test_get_by_persistence_id(
    session: Session,
):
    repository = RepositoryFixture(session)
    orm_object = repository.add("One Piece")
    repository.flush()

    restored = repository.get_by_id(
        orm_object.id
    )

    assert restored is orm_object


def test_get_by_persistence_id_returns_none(
    session: Session,
):
    repository = RepositoryFixture(session)

    assert repository.get_by_id(999) is None


def test_get_by_persistence_id_rejects_wrong_type(
    session: Session,
):
    repository = RepositoryFixture(session)

    with pytest.raises(TypeError):
        repository.get_by_id("1")


def test_one_or_none_query_helper(
    session: Session,
):
    repository = RepositoryFixture(session)
    repository.add("One Piece")
    repository.flush()

    restored = repository.get_by_name(
        "One Piece"
    )

    assert restored is not None
    assert restored.name == "One Piece"


def test_list_helper_returns_ordered_new_list(
    session: Session,
):
    repository = RepositoryFixture(session)
    repository.add("One Piece")
    repository.add("Naruto")
    repository.flush()

    first = repository.list_all()
    second = repository.list_all()

    assert [
        item.name for item in first
    ] == [
        "One Piece",
        "Naruto",
    ]
    assert first is not second


def test_exists_helper(
    session: Session,
):
    repository = RepositoryFixture(session)
    repository.add("One Piece")
    repository.flush()

    assert repository.exists_by_name(
        "One Piece"
    )
    assert not repository.exists_by_name(
        "Naruto"
    )


def test_delete_stages_row_removal(
    session: Session,
):
    repository = RepositoryFixture(session)
    orm_object = repository.add("One Piece")
    repository.flush()

    repository.delete(orm_object)
    repository.flush()

    assert repository.get_by_id(
        orm_object.id
    ) is None


def test_refresh_restores_database_state(
    session: Session,
):
    repository = RepositoryFixture(session)
    orm_object = repository.add("One Piece")
    repository.flush()

    session.execute(
        RepositoryFixtureORM.__table__.update()
        .where(
            RepositoryFixtureORM.id
            == orm_object.id
        )
        .values(name="One Piece Updated")
    )
    session.expire(orm_object)
    repository.refresh(orm_object)

    assert orm_object.name == "One Piece Updated"
