"""MangaTitle ORM persistence model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .chapter import ChapterORM
    from .series import SeriesORM


class MangaTitleORM(Base):
    """Relational persistence model for a MangaTitle."""

    __tablename__ = "manga_titles"
    __table_args__ = (
        UniqueConstraint(
            "series_id",
            "slug",
            name="uq_manga_titles_series_slug",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    series_id: Mapped[int] = mapped_column(
        ForeignKey("series.id"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    slug: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    series: Mapped[SeriesORM] = relationship(
        back_populates="manga_titles",
    )
    chapters: Mapped[list[ChapterORM]] = relationship(
        back_populates="manga_title",
    )