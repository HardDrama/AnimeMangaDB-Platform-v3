"""Chapter ORM persistence model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .episode_chapter_mapping import EpisodeChapterMappingORM
    from .manga_title import MangaTitleORM


class ChapterORM(Base):
    """Relational persistence model for a Chapter."""

    __tablename__ = "chapters"
    __table_args__ = (
        UniqueConstraint(
            "manga_title_id",
            "identifier",
            name="uq_chapters_manga_title_identifier",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    manga_title_id: Mapped[int] = mapped_column(
        ForeignKey("manga_titles.id"),
        nullable=False,
    )
    identifier: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )
    slug: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )

    manga_title: Mapped[MangaTitleORM] = relationship(
        back_populates="chapters",
    )
    episode_mappings: Mapped[
        list[EpisodeChapterMappingORM]
    ] = relationship(
        back_populates="chapter",
    )