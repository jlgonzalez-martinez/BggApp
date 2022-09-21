from dataclasses import dataclass, field
from typing import List

from boardgame.domain.events import Event


@dataclass
class Aggregate:
    version_number: int = 0
    events: List[Event] = field(default_factory=list)
