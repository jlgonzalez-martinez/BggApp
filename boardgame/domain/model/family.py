from dataclasses import dataclass

from boardgame.domain.model.aggregate import Aggregate


@dataclass
class Family(Aggregate):
    """Family class"""

    version_number: int = 0
    name: str = ""
    description: str = ""

    def __hash__(self):
        return hash(self.name)
