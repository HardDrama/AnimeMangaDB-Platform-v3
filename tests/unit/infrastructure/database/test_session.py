from sqlalchemy.orm import Session

from animemangadb.infrastructure.database.session import (
    SessionFactory,
)


def test_session_factory_creates_session():
    session = SessionFactory()

    try:
        assert isinstance(
            session,
            Session,
        )
    finally:
        session.close()


def test_session_factory_returns_new_sessions():
    first = SessionFactory()
    second = SessionFactory()

    try:
        assert first is not second
    finally:
        first.close()
        second.close()


def test_session_not_closed_on_creation():
    session = SessionFactory()

    try:
        assert session.is_active
    finally:
        session.close()


def test_session_factory_exists():
    assert SessionFactory is not None


def test_session_can_be_closed():
    session = SessionFactory()

    session.close()

    # Closing a Session is idempotent and should not raise.
    session.close()

    assert True