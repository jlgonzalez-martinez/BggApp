"""Boardgame client module to connect with the BGG."""
import logging
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import TYPE_CHECKING

import requests

from config import settings
from boardgame.adapters.clients.exceptions import BoardgameGeekException

if TYPE_CHECKING:
    from boardgame.adapters.clients.dto import BoardgameDto


class AbstractBggClient(ABC):
    """Abstract base class for the BGG client."""

    def __init__(self, api_url, logger, http_client=requests):
        self.api_url = api_url
        self.http_client = http_client
        self.logger = logger

    @classmethod
    def build(cls) -> "AbstractBggClient":
        """Build the client."""
        return cls(settings.bgg_url, logging.getLogger(__name__), http_client=requests)

    @abstractmethod
    def get(self, bgg_id: int) -> "BoardgameDto":
        """Get a boardgame from the BGG."""
        raise NotImplementedError

    def fetch(self, bgg_id: int) -> requests.Response:
        try:
            response = self.http_client.get(self.api_url + str(bgg_id))
            if response.status_code == HTTPStatus.OK:
                return response
            raise BoardgameGeekException(
                f"Api response {response.status_code} is not 200, raising error"
            )
        except Exception as ex:
            raise BoardgameGeekException(
                f"Bgg id {bgg_id} cannot be imported from the bgg."
            ) from ex
