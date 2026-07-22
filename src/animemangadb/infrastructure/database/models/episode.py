"""Episode ORM persistence model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .anime_title import AnimeTitleORM
    from .episode_chapter_mapping import EpisodeChapterMappingORM


class EpisodeORM(Base):
    """Relational persistence model for an Episode."""

    __tablename__ = "episodes"
    __table_args__ = (
        UniqueConstraint(
            "anime_title_id",
            "identifier",
            name="uq_episodes_anime_title_identifier",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    anime_title_id: Mapped[int] = mapped_column(
        ForeignKey("anime_titles.id"),
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

    anime_title: Mapped[AnimeTitleORM] = relationship(
        back_populates="episodes",
    )
    chapter_mappings: Mapped[
        list[EpisodeChapterMappingORM]
    ] = relationship(
        back_populates="episode",
    )