from dataclasses import dataclass, field
from typing import List

from boardgame.domain.events import Event


@dataclass
class Aggregate:
    """Aggregate class"""

    version_number: int = 0
    events: List[Event] = field(default_factory=list)
