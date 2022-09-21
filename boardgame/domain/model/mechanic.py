from dataclasses import dataclass

from boardgame.domain.model.aggregate import Aggregate


@dataclass
class Mechanic(Aggregate):
    """Mechanic class"""

    version_number: int = 0
    name: str = ""
    description: str = ""

    def __hash__(self):
        return hash(self.name)
