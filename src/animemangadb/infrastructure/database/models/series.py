"""Series ORM persistence model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .anime_title import AnimeTitleORM
    from .manga_title import MangaTitleORM


class SeriesORM(Base):
    """Relational persistence model for a Series."""

    __tablename__ = "series"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    slug: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        unique=True,
    )

    anime_titles: Mapped[list[AnimeTitleORM]] = relationship(
        back_populates="series",
    )
    manga_titles: Mapped[list[MangaTitleORM]] = relationship(
        back_populates="series",
    )