from dataclasses import dataclass


@dataclass
class Stat:
    """Boardgame stats class"""

    std_dev: float = 0
    median: float = 0
    owned: int = 0
    trading: int = 0
    wanting: int = 0
    wishing: int = 0
    weight_average: float = 0
    rating_average: float = 0
    bayes_average: float = 0
    num_rates: int = 0
    num_comments: int = 0
    num_weights: int = 0
