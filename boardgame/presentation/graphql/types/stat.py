from typing import TYPE_CHECKING

import strawberry

from .domain_type import DomainType

if TYPE_CHECKING:
    from boardgame.domain.model import Stat


@strawberry.type
class StatType(DomainType):
    """Stat type."""

    std_dev: float
    median: float
    owned: int
    trading: int
    wanting: int
    wishing: int
    weight_average: float
    rating_average: float
    bayes_average: float
    num_rates: int
    num_comments: int
    num_weights: int

    @classmethod
    def from_domain(cls, instance: "Stat") -> "StatType":
        """Convert a domain stat to a type."""
        return cls(
            std_dev=instance.std_dev,
            median=instance.median,
            owned=instance.owned,
            trading=instance.trading,
            wanting=instance.wanting,
            wishing=instance.wishing,
            weight_average=instance.weight_average,
            rating_average=instance.rating_average,
            bayes_average=instance.bayes_average,
            num_rates=instance.num_rates,
            num_comments=instance.num_comments,
            num_weights=instance.num_weights,
        )
