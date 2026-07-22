"""Mapping policy for Domain and ORM conversion."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MappingPolicy:
    """Rules shared by all Domain and ORM entity mappers.

    Entity mappers perform shallow conversion. Repositories are
    responsible for resolving relationships and composing complete
    object graphs.
    """

    map_scalar_fields: bool = True
    map_relationships: bool = False
    preserve_persistence_identity: bool = False
    repository_composes_object_graphs: bool = True


DEFAULT_MAPPING_POLICY = MappingPolicy()
