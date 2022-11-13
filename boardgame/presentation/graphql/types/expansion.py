from typing import TYPE_CHECKING

import strawberry

from .domain_type import DomainType

if TYPE_CHECKING:
    from boardgame.domain.model import Expansion


@strawberry.type
class ExpansionType(DomainType):
    """Category type."""

    bgg_id: int
    name: str

    @classmethod
    def from_domain(cls, instance: "Expansion") -> "ExpansionType":
        """Convert a domain expansion to a type."""
        return cls(bgg_id=instance.bgg_id, name=instance.name)
