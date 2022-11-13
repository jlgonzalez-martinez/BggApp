from typing import TYPE_CHECKING

import strawberry

from .domain_type import DomainType

if TYPE_CHECKING:
    from boardgame.domain.model import LanguageDependence


@strawberry.type
class LanguageDependenceType(DomainType):
    """Language dependence type."""

    very_low: int
    low: int
    medium: int
    high: int
    very_high: int

    @classmethod
    def from_domain(cls, instance: "LanguageDependence") -> "LanguageDependenceType":
        """Convert a domain language dependence to a type."""
        return cls(
            very_low=instance.very_low,
            low=instance.low,
            medium=instance.medium,
            high=instance.high,
            very_high=instance.very_high,
        )
