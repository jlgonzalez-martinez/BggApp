from dataclasses import dataclass
from typing import Optional
from unittest.mock import MagicMock


@dataclass
class FakeHttpClient:
    """Fake HTTP client."""

    response: Optional[MagicMock] = None
    url: str = ""

    def get(self, url: str) -> MagicMock:
        """Fake get method."""
        self.url = url
        return self.response
