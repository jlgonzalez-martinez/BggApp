from typing import TYPE_CHECKING

import strawberry

from .domain_type import DomainType

if TYPE_CHECKING:
    from boardgame.domain.model import Family


@strawberry.type
class FamilyType(DomainType):
    """Category type."""

    id: strawberry.ID
    name: str
    description: str

    @classmethod
    def from_domain(cls, instance: "Family") -> "FamilyType":
        """Convert a domain family to a type."""
        return cls(
            id=getattr(instance, "id", None),
            name=instance.name,
            description=instance.description,
        )
