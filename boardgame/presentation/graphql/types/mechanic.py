from typing import TYPE_CHECKING

import strawberry

from .domain_type import DomainType

if TYPE_CHECKING:
    from boardgame.domain.model import Mechanic


@strawberry.type
class MechanicType(DomainType):
    """Category type."""

    id: strawberry.ID
    name: str
    description: str

    @classmethod
    def from_domain(cls, mechanic: "Mechanic") -> "MechanicType":
        """Convert a domain mechanic to a type."""
        return cls(
            id=getattr(mechanic, "id", None),
            name=mechanic.name,
            description=mechanic.description,
        )
