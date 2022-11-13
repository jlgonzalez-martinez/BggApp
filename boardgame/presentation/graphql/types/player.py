from typing import TYPE_CHECKING

import strawberry

from .domain_type import DomainType

if TYPE_CHECKING:
    from boardgame.domain.model import Player


@strawberry.type
class PlayerType(DomainType):
    """Num players class"""

    number: int
    best: int
    recommended: int
    not_recommended: int

    @classmethod
    def from_domain(cls, instance: "Player") -> "PlayerType":
        """Convert a domain player to a type."""
        return cls(
            number=instance.number,
            best=instance.best,
            recommended=instance.recommended,
            not_recommended=instance.not_recommended,
        )
