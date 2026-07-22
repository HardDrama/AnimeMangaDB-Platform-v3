"""EpisodeChapterMapping ORM persistence model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .chapter import ChapterORM
    from .episode import EpisodeORM


class EpisodeChapterMappingORM(Base):
    """Relational persistence model for an Episode–Chapter mapping."""

    __tablename__ = "episode_chapter_mappings"
    __table_args__ = (
        UniqueConstraint(
            "episode_id",
            "chapter_id",
            name=(
                "uq_episode_chapter_mappings_"
                "episode_chapter"
            ),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    episode_id: Mapped[int] = mapped_column(
        ForeignKey("episodes.id"),
        nullable=False,
    )
    chapter_id: Mapped[int] = mapped_column(
        ForeignKey("chapters.id"),
        nullable=False,
    )

    episode: Mapped[EpisodeORM] = relationship(
        back_populates="chapter_mappings",
    )
    chapter: Mapped[ChapterORM] = relationship(
        back_populates="episode_mappings",
    )